import { Check, Copy } from "lucide-react";
import { useState } from "react";

interface MathBlockProps {
  formula: string;
  name?: string;
  explanation?: string;
}

export function MathBlock({ formula, name, explanation }: MathBlockProps) {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(formula);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="rounded-lg border border-[#222228] bg-[#0A0A0C] p-4">
      <div className="flex items-center justify-between border-b border-[#222228] pb-2 mb-2.5">
        <span className="font-mono text-xs font-bold uppercase tracking-wider text-[#10B981]">
          {name || "Mathematical Formulation"}
        </span>
        <button
          onClick={handleCopy}
          className="flex items-center gap-1 rounded border border-[#27272A] bg-[#111115] px-2 py-0.5 text-[10px] text-[#A1A1AA] hover:text-white"
        >
          {copied ? <Check className="h-3 w-3 text-[#10B981]" /> : <Copy className="h-3 w-3" />}
          <span>{copied ? "Copied" : "Copy"}</span>
        </button>
      </div>

      <div className="overflow-x-auto rounded bg-[#111115] p-3 font-mono text-sm text-[#E4E4E7] border border-[#27272A]">
        <code>{formula}</code>
      </div>

      {explanation && (
        <p className="mt-2 text-xs leading-relaxed text-[#A1A1AA]">
          {explanation}
        </p>
      )}
    </div>
  );
}
