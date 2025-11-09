import * as React from "react";
import { useState, useEffect } from "react";
import ProjectCard from "../components/ProjectCard";

const sampleProjects = [
  {
    id: 2,
    name: "collab-hub",
    description:
      "AI-powered team collaboration dashboard that helps hackathon teams brainstorm, assign tasks, and track progress in real time.",
    updatedAt: "1 day ago",
    link: "#",
    tech: ["React", "Vite", "Tailwind", "Express", "OpenAI API"],
    visibility: "public",
  },
  {
    id: 3,
    name: "taskgenie",
    description:
      "Generates and prioritizes hackathon tasks using AI — just describe your project, and it builds the roadmap for you.",
    updatedAt: "3 hours ago",
    link: "#",
    tech: ["React", "Vite", "Tailwind", "FastAPI", "OpenAI API"],
    visibility: "public",
  },
  {
    id: 4,
    name: "buildpulse",
    description:
      "A smart analytics dashboard that visualizes team performance, code commits, and sprint velocity during hackathons.",
    updatedAt: "5 hours ago",
    link: "#",
    tech: ["React", "Vite", "Chart.js", "Node.js"],
    visibility: "public",
  },
  {
    id: 5,
    name: "hackmap",
    description:
      "Interactive real-time map showing global hackathon events, projects, and team stats powered by open APIs.",
    updatedAt: "4 days ago",
    link: "#",
    tech: ["React", "Vite", "Leaflet", "Supabase"],
    visibility: "public",
  },
  {
    id: 6,
    name: "promptboard",
    description:
      "A shared AI prompt board for brainstorming ideas and generating creative solutions during hackathons.",
    updatedAt: "6 hours ago",
    link: "#",
    tech: ["React", "Vite", "Firebase", "Tailwind"],
    visibility: "public",
  },
  {
    id: 7,
    name: "visionify",
    description:
      "Computer vision demo app that detects objects and tracks team equipment using live webcam feeds.",
    updatedAt: "3 days ago",
    link: "#",
    tech: ["React", "TensorFlow.js", "Vite", "Tailwind"],
    visibility: "public",
  },
  {
    id: 8,
    name: "devsync",
    description:
      "Lightweight hub for syncing commits, tasks, and chat messages across GitHub, Slack, and Trello in one interface.",
    updatedAt: "8 hours ago",
    link: "#",
    tech: ["React", "Vite", "Tailwind", "GraphQL"],
    visibility: "public",
  },
  {
    id: 9,
    name: "aura-note",
    description:
      "AI mood-based journaling app that helps teams reflect and stay motivated throughout the hackathon.",
    updatedAt: "2 days ago",
    link: "#",
    tech: ["React", "Vite", "Tailwind", "Flask"],
    visibility: "public",
  },
];

const SkeletonCard = () => {
  return (
    <div className="min-h-[200px] border border-[#363636] rounded-sm p-6 bg-[#0a0a0a] flex flex-col justify-between animate-pulse">
      <div>
        <div className="h-6 bg-gray-800 rounded w-3/4 mb-2"></div>
        <div className="h-4 bg-gray-800 rounded w-full mb-1"></div>
        <div className="h-4 bg-gray-800 rounded w-5/6"></div>

        <div className="flex gap-2 mt-4">
          <div className="h-6 w-16 bg-gray-800 rounded"></div>
          <div className="h-6 w-20 bg-gray-800 rounded"></div>
          <div className="h-6 w-16 bg-gray-800 rounded"></div>
        </div>
      </div>

      <div className="flex justify-between items-center mt-4">
        <div className="h-3 bg-gray-800 rounded w-24"></div>
      </div>
    </div>
  );
};

const Dashboard = () => {
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Simulate loading delay
    const timer = setTimeout(() => {
      setIsLoading(false);
    }, 1200); // 1.2 seconds loading

    return () => clearTimeout(timer);
  }, []);

  return (
    <div className="p-12 animate-fade-in">
      <div
        className="flex items-center justify-between mb-6 animate-slide-down opacity-0"
        style={{ animationDelay: "0.1s" }}
      >
        <h1 className="text-2xl text-nvidia font-semibold">Projects</h1>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
        {isLoading
          ? // Show skeleton cards while loading
            Array.from({ length: 8 }).map((_, index) => (
              <div
                key={`skeleton-${index}`}
                className="animate-fade-in"
                style={{ animationDelay: `${index * 0.05}s` }}
              >
                <SkeletonCard />
              </div>
            ))
          : // Show actual project cards after loading
            sampleProjects.map((p, index) => (
              <div
                key={p.id}
                className="animate-scale-in opacity-0"
                style={{ animationDelay: `${0.1 + index * 0.05}s` }}
              >
                <ProjectCard project={p} />
              </div>
            ))}
      </div>
    </div>
  );
};

export default Dashboard;
