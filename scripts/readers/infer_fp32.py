"""Run vesuvius ink inference in true fp32.

The upstream infer.py wraps the forward pass in torch.autocast("cuda", dtype=None)
even when --amp-dtype default/auto resolves to "no AMP", which silently enables
fp16 autocast. On GTX 16xx GPUs fp16 yields NaNs, so this wrapper turns autocast
off whenever no dtype is requested. Same CLI as vesuvius.ink_detection.inference.infer.
"""
import runpy
import sys

import torch

_OrigAutocast = torch.autocast


class _Fp32WhenNoDtype(_OrigAutocast):
    def __init__(self, device_type, dtype=None, enabled=True, cache_enabled=None):
        if dtype is None and device_type == "cuda":
            enabled = False
        super().__init__(device_type, dtype=dtype, enabled=enabled, cache_enabled=cache_enabled)


torch.autocast = _Fp32WhenNoDtype
sys.argv = ["vesuvius.ink_detection.inference.infer"] + sys.argv[1:]
runpy.run_module("vesuvius.ink_detection.inference.infer", run_name="__main__", alter_sys=True)
