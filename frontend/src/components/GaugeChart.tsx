"use client";

import { motion } from "framer-motion";

interface GaugeChartProps {
  value: number; // 0 - 100
  title: string;
  subtitle?: string;
  size?: number;
  color?: string;
}

export function GaugeChart({
  value,
  title,
  subtitle,
  size = 140,
  color = "#10B981"
}: GaugeChartProps) {
  const strokeWidth = 10;
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (value / 100) * circumference;

  return (
    <div className="flex flex-col items-center justify-center p-3 text-center">
      <div className="relative flex items-center justify-center" style={{ width: size, height: size }}>
        <svg width={size} height={size} className="rotate-[-90deg]">
          {/* Track background */}
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            stroke="#222228"
            strokeWidth={strokeWidth}
            fill="transparent"
          />
          {/* Value stroke */}
          <motion.circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            stroke={color}
            strokeWidth={strokeWidth}
            strokeDasharray={circumference}
            initial={{ strokeDashoffset: circumference }}
            animate={{ strokeDashoffset: offset }}
            transition={{ duration: 1.2, ease: "easeOut" }}
            strokeLinecap="round"
            fill="transparent"
          />
        </svg>

        {/* Center label */}
        <div className="absolute flex flex-col items-center justify-center">
          <motion.span
            initial={{ opacity: 0, scale: 0.5 }}
            animate={{ opacity: 1, scale: 1 }}
            className="font-mono text-2xl font-black text-white"
          >
            {value.toFixed(1)}%
          </motion.span>
        </div>
      </div>

      <div className="mt-2.5">
        <h4 className="font-mono text-xs font-bold uppercase tracking-wider text-white">{title}</h4>
        {subtitle && <p className="text-[11px] text-[#A1A1AA]">{subtitle}</p>}
      </div>
    </div>
  );
}
