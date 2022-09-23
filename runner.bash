#!/usr/bin/bash
# Quick and dirty method to schedule recordings of the afternoon
# commercial-free block. Update crontab with:
#   30 15 * * * /home/joe/projects/radio-record/runner.bash
# (Hot 97.1 is Eastern time but my machine is UTC)
# Note to self: This will break when DST ends...

src_dir=/home/joe/projects/radio-record
venv_bin=/home/joe/.local/share/virtualenvs/radio-record-E4CsiPAu/bin

cd "${src_dir}"
"${venv_bin}/python" \
    "${src_dir}/main.py" \
    --duration "3 hours" \
    >> "${src_dir}/stdout.txt" \
    2>> "${src_dir}/stderr.txt"
