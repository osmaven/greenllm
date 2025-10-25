
#!/usr/bin/env python
import argparse, json, os, sys
from framework.src.greenllm.runners.inference_runner import run_measurement
from framework.src.greenllm.metrics.metrics import compute_metrics

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="TinyLlama/TinyLlama-1.1B-Chat-v1.0")
    ap.add_argument("--prompts", default="data/prompts/prompt_set_small.txt")
    ap.add_argument("--max-new-tokens", type=int, default=64)
    ap.add_argument("--meter", default="none")
    ap.add_argument("--ci", type=float, default=300.0)
    args = ap.parse_args()

    res = run_measurement(args.model, args.prompts, max_new_tokens=args.max_new_tokens, meter_name=args.meter, carbon_intensity=args.ci)
    met = compute_metrics(res)
    print(json.dumps({**res, **met}, indent=2))

if __name__ == "__main__":
    main()
