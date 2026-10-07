"use client";

import { useState, useCallback } from "react";
import {
  ReactFlow,
  MiniMap,
  Controls,
  Background,
  useNodesState,
  useEdgesState,
  addEdge,
  Node,
  Edge,
  MarkerType
} from "@xyflow/react";
import "@xyflow/react/dist/style.css";
import { Network, ZoomIn, Info, Star, Compass, Layers, CheckCircle } from "lucide-react";
import { SKILL_NODES } from "@/lib/data";
import { MathBlock } from "@/components/MathBlock";

const INITIAL_NODES: Node[] = [
  {
    id: "python",
    position: { x: 50, y: 180 },
    data: { label: "Python", category: "Core", pageRank: 0.142, centrality: 18, difficulty: "Foundational" },
    style: { background: "#111115", color: "#FFF", border: "2px solid #10B981", borderRadius: "8px", padding: "12px", width: 140 }
  },
  {
    id: "sql",
    position: { x: 50, y: 320 },
    data: { label: "SQL", category: "Database", pageRank: 0.128, centrality: 16, difficulty: "Foundational" },
    style: { background: "#111115", color: "#FFF", border: "1px solid #27272A", borderRadius: "8px", padding: "12px", width: 130 }
  },
  {
    id: "pandas",
    position: { x: 260, y: 100 },
    data: { label: "Pandas", category: "Data", pageRank: 0.088, centrality: 12, difficulty: "Foundational" },
    style: { background: "#111115", color: "#FFF", border: "1px solid #27272A", borderRadius: "8px", padding: "10px", width: 130 }
  },
  {
    id: "numpy",
    position: { x: 260, y: 220 },
    data: { label: "NumPy", category: "Data", pageRank: 0.082, centrality: 11, difficulty: "Foundational" },
    style: { background: "#111115", color: "#FFF", border: "1px solid #27272A", borderRadius: "8px", padding: "10px", width: 130 }
  },
  {
    id: "fastapi",
    position: { x: 260, y: 340 },
    data: { label: "FastAPI", category: "Backend", pageRank: 0.076, centrality: 10, difficulty: "Intermediate" },
    style: { background: "#111115", color: "#FFF", border: "1px solid #27272A", borderRadius: "8px", padding: "10px", width: 130 }
  },
  {
    id: "scikit-learn",
    position: { x: 470, y: 160 },
    data: { label: "Machine Learning (Scikit-Learn)", category: "ML", pageRank: 0.095, centrality: 14, difficulty: "Intermediate" },
    style: { background: "#111115", color: "#FFF", border: "1.5px solid #E03590", borderRadius: "8px", padding: "12px", width: 170 }
  },
  {
    id: "pytorch",
    position: { x: 700, y: 100 },
    data: { label: "PyTorch Deep Learning", category: "Deep Learning", pageRank: 0.114, centrality: 16, difficulty: "Advanced" },
    style: { background: "#111115", color: "#FFF", border: "2px solid #10B981", borderRadius: "8px", padding: "12px", width: 180 }
  },
  {
    id: "docker",
    position: { x: 470, y: 340 },
    data: { label: "Docker & Containers", category: "DevOps", pageRank: 0.092, centrality: 15, difficulty: "Intermediate" },
    style: { background: "#111115", color: "#FFF", border: "1px solid #27272A", borderRadius: "8px", padding: "10px", width: 150 }
  },
  {
    id: "transformers",
    position: { x: 940, y: 100 },
    data: { label: "Transformers & LLMs", category: "GenAI", pageRank: 0.098, centrality: 14, difficulty: "Advanced" },
    style: { background: "#111115", color: "#FFF", border: "1.5px solid #10B981", borderRadius: "8px", padding: "12px", width: 160 }
  },
  {
    id: "mlops",
    position: { x: 700, y: 280 },
    data: { label: "MLOps & CI/CD", category: "DevOps", pageRank: 0.094, centrality: 14, difficulty: "Advanced" },
    style: { background: "#111115", color: "#FFF", border: "1px solid #27272A", borderRadius: "8px", padding: "12px", width: 150 }
  },
  {
    id: "rag",
    position: { x: 1150, y: 180 },
    data: { label: "RAG & LLMOps Architectures", category: "GenAI", pageRank: 0.105, centrality: 15, difficulty: "Expert" },
    style: { background: "#18181D", color: "#10B981", border: "2px solid #10B981", borderRadius: "8px", padding: "14px", width: 190, fontWeight: "bold" }
  }
];

const INITIAL_EDGES: Edge[] = [
  { id: "e-py-pd", source: "python", target: "pandas", animated: true, style: { stroke: "#10B981" }, markerEnd: { type: MarkerType.ArrowClosed, color: "#10B981" } },
  { id: "e-py-np", source: "python", target: "numpy", animated: true, style: { stroke: "#10B981" }, markerEnd: { type: MarkerType.ArrowClosed, color: "#10B981" } },
  { id: "e-py-fa", source: "python", target: "fastapi", style: { stroke: "#71717A" }, markerEnd: { type: MarkerType.ArrowClosed, color: "#71717A" } },
  { id: "e-pd-skl", source: "pandas", target: "scikit-learn", style: { stroke: "#71717A" }, markerEnd: { type: MarkerType.ArrowClosed, color: "#71717A" } },
  { id: "e-np-skl", source: "numpy", target: "scikit-learn", style: { stroke: "#71717A" }, markerEnd: { type: MarkerType.ArrowClosed, color: "#71717A" } },
  { id: "e-skl-pt", source: "scikit-learn", target: "pytorch", animated: true, style: { stroke: "#10B981" }, markerEnd: { type: MarkerType.ArrowClosed, color: "#10B981" } },
  { id: "e-pt-tf", source: "pytorch", target: "transformers", animated: true, style: { stroke: "#10B981" }, markerEnd: { type: MarkerType.ArrowClosed, color: "#10B981" } },
  { id: "e-tf-rag", source: "transformers", target: "rag", animated: true, style: { stroke: "#10B981", strokeWidth: 2 }, markerEnd: { type: MarkerType.ArrowClosed, color: "#10B981" } },
  { id: "e-fa-rag", source: "fastapi", target: "rag", style: { stroke: "#71717A" }, markerEnd: { type: MarkerType.ArrowClosed, color: "#71717A" } },
  { id: "e-doc-mlops", source: "docker", target: "mlops", style: { stroke: "#71717A" }, markerEnd: { type: MarkerType.ArrowClosed, color: "#71717A" } },
  { id: "e-fa-mlops", source: "fastapi", target: "mlops", style: { stroke: "#71717A" }, markerEnd: { type: MarkerType.ArrowClosed, color: "#71717A" } },
  { id: "e-mlops-rag", source: "mlops", target: "rag", style: { stroke: "#71717A" }, markerEnd: { type: MarkerType.ArrowClosed, color: "#71717A" } }
];

export default function KnowledgeGraphPage() {
  const [nodes, setNodes, onNodesChange] = useNodesState(INITIAL_NODES);
  const [edges, setEdges, onEdgesChange] = useEdgesState(INITIAL_EDGES);
  const [selectedNode, setSelectedNode] = useState<any>(INITIAL_NODES[0]);

  const onNodeClick = useCallback((event: any, node: Node) => {
    setSelectedNode(node);
  }, []);

  return (
    <div className="space-y-8 pb-12">
      {/* Header */}
      <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between border-b border-[#222228] pb-5">
        <div>
          <div className="flex items-center gap-2">
            <Network className="h-5 w-5 text-[#10B981]" />
            <span className="font-mono text-xs font-semibold uppercase tracking-wider text-[#10B981]">
              Page 3 — Knowledge Graph Topology
            </span>
          </div>
          <h1 className="text-2xl font-black text-white mt-1">
            Workforce Skill Dependency & Centrality Explorer
          </h1>
          <p className="text-xs text-[#A1A1AA]">
            Interactive directed acyclic graph (DAG) modeling prerequisite trees, PageRank topological importance, and hidden upskilling paths.
          </p>
        </div>

        <div className="flex items-center gap-2 font-mono text-xs">
          <span className="rounded bg-[#111115] px-3 py-1.5 border border-[#27272A] text-white">
            38 Nodes · 40 Edges
          </span>
        </div>
      </div>

      {/* Main Interactive Canvas & Inspector */}
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-12">
        {/* Canvas Area */}
        <div className="h-[520px] rounded-xl border border-[#222228] bg-[#0A0A0C] p-1 lg:col-span-8 overflow-hidden relative shadow-2xl">
          <ReactFlow
            nodes={nodes}
            edges={edges}
            onNodesChange={onNodesChange}
            onEdgesChange={onEdgesChange}
            onNodeClick={onNodeClick}
            fitView
          >
            <Controls className="!bg-[#111115] !border-[#27272A] !fill-white" />
            <MiniMap
              nodeColor="#10B981"
              maskColor="rgba(10, 10, 12, 0.8)"
              className="!bg-[#111115] !border-[#27272A] rounded"
            />
            <Background color="#222228" gap={20} size={1} />
          </ReactFlow>
        </div>

        {/* Selected Node Deep Inspector */}
        <div className="flex flex-col justify-between rounded-xl border border-[#222228] bg-[#111115] p-5 lg:col-span-4">
          <div className="space-y-4">
            <div className="border-b border-[#222228] pb-3">
              <span className="font-mono text-[10px] uppercase text-[#10B981] font-bold">
                Selected Node Inspector
              </span>
              <h3 className="text-xl font-bold text-white mt-1 font-mono">
                {selectedNode?.data?.label || "Python"}
              </h3>
              <span className="inline-block mt-1 rounded bg-[#27272A] px-2 py-0.5 font-mono text-[10px] text-[#A1A1AA]">
                {selectedNode?.data?.category || "Core Language"}
              </span>
            </div>

            <div className="space-y-3">
              <div className="flex justify-between border-b border-[#222228] pb-2 text-xs font-mono">
                <span className="text-[#A1A1AA]">PageRank Score:</span>
                <span className="font-bold text-[#10B981]">{selectedNode?.data?.pageRank || 0.142}</span>
              </div>
              <div className="flex justify-between border-b border-[#222228] pb-2 text-xs font-mono">
                <span className="text-[#A1A1AA]">Degree Centrality:</span>
                <span className="font-bold text-white">{selectedNode?.data?.centrality || 18} Links</span>
              </div>
              <div className="flex justify-between border-b border-[#222228] pb-2 text-xs font-mono">
                <span className="text-[#A1A1AA]">Difficulty Tier:</span>
                <span className="font-bold text-white">{selectedNode?.data?.difficulty || "Foundational"}</span>
              </div>
            </div>

            <div className="rounded-md border border-[#27272A] bg-[#0A0A0C] p-3 text-xs text-[#A1A1AA]">
              <strong className="text-white">Topological Role:</strong> High-influence anchor competency that serves as a direct prerequisite for 6 downstream AI frameworks.
            </div>
          </div>

          <div className="mt-4 pt-3 border-t border-[#222228]">
            <span className="font-mono text-[10px] text-[#71717A] uppercase">Navigation Shortcut</span>
            <p className="text-xs text-[#E4E4E7] mt-1">
              Select any node in the graph to inspect structural connectivity and centrality.
            </p>
          </div>
        </div>
      </div>

      {/* Top 5 Critical Anchors Table */}
      <div className="rounded-xl border border-[#222228] bg-[#111115] p-5">
        <h3 className="font-mono text-sm font-bold text-white mb-3">
          Critical Anchor Skills by Composite Centrality & PageRank
        </h3>
        <div className="overflow-x-auto">
          <table className="w-full text-left font-mono text-xs">
            <thead>
              <tr className="border-b border-[#222228] text-[#71717A]">
                <th className="pb-2.5">Skill Node</th>
                <th className="pb-2.5">Category</th>
                <th className="pb-2.5">PageRank Index</th>
                <th className="pb-2.5">Degree Centrality</th>
                <th className="pb-2.5">Historical Growth CAGR</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#222228]">
              {SKILL_NODES.slice(0, 6).map((node) => (
                <tr key={node.id} className="hover:bg-[#18181D]">
                  <td className="py-2.5 font-bold text-white">{node.label}</td>
                  <td className="py-2.5 text-[#A1A1AA]">{node.category}</td>
                  <td className="py-2.5 text-[#10B981] font-bold">{node.pageRank.toFixed(3)}</td>
                  <td className="py-2.5 text-white">{node.degreeCentrality} Connections</td>
                  <td className="py-2.5 text-[#10B981]">+{node.historicalGrowthCAGR}%</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Mathematical Breakdown */}
      <MathBlock
        name="PageRank & Composite Graph Centrality"
        formula="\mathbf{PR}(v_i) = \frac{1 - d}{|V|} + d \sum_{v_j \in \mathcal{M}(v_i)} \frac{\mathbf{PR}(v_j)}{L(v_j)}"
        explanation="Damping factor d = 0.85. Evaluates the steady-state probability of visiting each skill node across the workforce dependency topology."
      />
    </div>
  );
}
