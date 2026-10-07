"use client";

import { motion } from "framer-motion";

interface TraitPoint {
  trait: string;
  value: number; // 0 - 10 scale
}

interface RadarChartProps {
  currentTraits: TraitPoint[];
  futureTraits?: TraitPoint[];
  size?: number;
  showLegend?: boolean;
}

export function RadarChart({
  currentTraits,
  futureTraits,
  size = 280,
  showLegend = true
}: RadarChartProps) {
  const center = size / 2;
  const radius = size * 0.38;
  const count = currentTraits.length;
  const angleStep = (2 * Math.PI) / count;

  // Compute coordinate points
  const getCoordinates = (traits: TraitPoint[]) => {
    return traits.map((t, idx) => {
      const angle = idx * angleStep - Math.PI / 2;
      const normalized = Math.min(10, Math.max(0, t.value)) / 10;
      const r = normalized * radius;
      return {
        x: center + r * Math.cos(angle),
        y: center + r * Math.sin(angle),
        trait: t.trait,
        val: t.value
      };
    });
  };

  const currentCoords = getCoordinates(currentTraits);
  const futureCoords = futureTraits ? getCoordinates(futureTraits) : null;

  const currentPath = currentCoords.map((c, i) => `${i === 0 ? "M" : "L"} ${c.x} ${c.y}`).join(" ") + " Z";
  const futurePath = futureCoords ? futureCoords.map((c, i) => `${i === 0 ? "M" : "L"} ${c.x} ${c.y}`).join(" ") + " Z" : null;

  // Grid levels (20%, 40%, 60%, 80%, 100%)
  const gridLevels = [0.2, 0.4, 0.6, 0.8, 1.0];

  return (
    <div className="flex flex-col items-center justify-center p-2">
      <svg width={size} height={size} className="overflow-visible">
        {/* Concentric grid rings */}
        {gridLevels.map((lvl, i) => (
          <polygon
            key={i}
            points={currentTraits
              .map((_, idx) => {
                const angle = idx * angleStep - Math.PI / 2;
                const r = lvl * radius;
                return `${center + r * Math.cos(angle)},${center + r * Math.sin(angle)}`;
              })
              .join(" ")}
            fill="transparent"
            stroke="#222228"
            strokeWidth={1}
            strokeDasharray={i === gridLevels.length - 1 ? "0" : "2 2"}
          />
        ))}

        {/* Radial Axis lines */}
        {currentTraits.map((_, idx) => {
          const angle = idx * angleStep - Math.PI / 2;
          const x = center + radius * Math.cos(angle);
          const y = center + radius * Math.sin(angle);
          return <line key={idx} x1={center} y1={center} x2={x} y2={y} stroke="#222228" strokeWidth={1} />;
        })}

        {/* Future State Polygon (if provided) */}
        {futurePath && (
          <motion.path
            d={futurePath}
            fill="rgba(16, 185, 129, 0.25)"
            stroke="#10B981"
            strokeWidth={2}
            strokeDasharray="4 4"
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.8 }}
          />
        )}

        {/* Current State Polygon */}
        <motion.path
          d={currentPath}
          fill="rgba(255, 255, 255, 0.15)"
          stroke="#FFFFFF"
          strokeWidth={2}
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.8 }}
        />

        {/* Data points */}
        {currentCoords.map((c, i) => (
          <circle key={i} cx={c.x} cy={c.y} r={3.5} fill="#FFFFFF" />
        ))}
        {futureCoords &&
          futureCoords.map((c, i) => (
            <circle key={`f-${i}`} cx={c.x} cy={c.y} r={3.5} fill="#10B981" />
          ))}

        {/* Trait labels */}
        {currentTraits.map((t, idx) => {
          const angle = idx * angleStep - Math.PI / 2;
          const labelDist = radius + 22;
          const lx = center + labelDist * Math.cos(angle);
          const ly = center + labelDist * Math.sin(angle);

          return (
            <text
              key={t.trait}
              x={lx}
              y={ly}
              textAnchor="middle"
              dominantBaseline="middle"
              className="fill-[#A1A1AA] font-mono text-[10px] font-semibold"
            >
              {t.trait} ({t.value})
            </text>
          );
        })}
      </svg>

      {showLegend && (
        <div className="mt-4 flex items-center gap-5 text-xs font-mono">
          <div className="flex items-center gap-1.5">
            <span className="h-2.5 w-2.5 rounded-sm bg-white"></span>
            <span className="text-[#A1A1AA]">Current State</span>
          </div>
          {futureTraits && (
            <div className="flex items-center gap-1.5">
              <span className="h-2.5 w-2.5 rounded-sm bg-[#10B981]"></span>
              <span className="text-[#10B981]">Simulated Digital Twin</span>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
