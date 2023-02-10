from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import tempfile
import os
import json
from labelbase.models import Labelbase, Label
from labelbase.serializers import LabelSerializer
from django.shortcuts import get_object_or_404
from django.contrib import messages


from .forms import UploadFileForm
from tempfile import NamedTemporaryFile

EOLSTOP = [b'', '', None, '\n']

def handle_uploaded_file(f):
    fp = NamedTemporaryFile(delete=False)
    for chunk in f.chunks():
        fp.write(chunk)
    return fp



@login_required
def upload_labels(request):
    """
    Used to import labels manually using files.
    """
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            imported_lables = 0
            labelbase = get_object_or_404(Labelbase, id=form.cleaned_data.get('labelbase_id', ''), user_id=request.user.id)
            fp = handle_uploaded_file(request.FILES['file'])
            fp.seek(0)
            # BIP-0329
            if form.cleaned_data.get('import_type', '') == 'BIP-0329':
                while True:
                    buf = fp.readline()
                    if buf in EOLSTOP:
                        break
                    data = json.loads(buf)
                    data['labelbase'] = labelbase.id
                    serializer = LabelSerializer(data=data)
                    if serializer.is_valid():
                        serializer.save()
                        imported_lables += 1
            # BlueWallet
            elif form.cleaned_data.get('import_type', '') == 'csv-bluewallet':
                while True:
                    buf = fp.readline()
                    if buf in EOLSTOP:
                        break
                    sbuf = str(buf).split(",")
                    data = {
                        'type': 'tx',
                        'ref': sbuf[1],
                        'label': sbuf[3:],
                    }
                    data['labelbase'] = labelbase.id
                    serializer = LabelSerializer(data=data)
                    if serializer.is_valid():
                        serializer.save()
                        imported_lables += 1
            else:
                fp.close()
                os.unlink(fp.name)
                return HttpResponseRedirect('/failed/url/')
            fp.close()
            os.unlink(fp.name)
            if imported_lables:
                messages.add_message(request, messages.INFO, "Processed and imported {} labels.".format(imported_lables))
            return HttpResponseRedirect(labelbase.get_absolute_url())
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})
