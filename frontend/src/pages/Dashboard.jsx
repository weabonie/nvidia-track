import * as React from "react";
import { useState, useEffect } from "react";
import axios from "axios";
import ProjectCard from "../components/ProjectCard";
import DeployModal from "../components/DeployModal";

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
  const [projects, setProjects] = useState([]);
  const [error, setError] = useState(null);
  const [activeSection, setActiveSection] = useState("projects");
  const [showDeployModal, setShowDeployModal] = useState(false);

  useEffect(() => {
    const fetchProjects = async () => {
      try {
        const response = await axios.get("https://apihackutd.siru.dev/repos");
        const formattedProjects = response.data.map((project) => ({
          id: project.id,
          name: project.name,
          description: project.description || "No description provided",
          updatedAt: "Recently updated",
          tech: project.languages || [],
          visibility: project.private ? "private" : "public",
          link: project.html_url,
        }));
        setProjects(formattedProjects);
        setIsLoading(false);
      } catch (err) {
        console.error("Error fetching projects:", err);
        setError("Failed to load projects");
        setIsLoading(false);
      }
    };

    fetchProjects();
  }, []);

  return (
    <div className="animate-fade-in">
      <div className="px-6 lg:px-8 max-w-7xl mx-auto">
        <div
          className="flex items-center justify-between mb-6 animate-slide-down opacity-0"
          style={{ animationDelay: "0.1s" }}
        >
          <div className="py-6">
            <h1 className="text-2xl text-white font-semibold mb-3">
              My Projects
            </h1>
            <p className="text-sm text-gray-400">
              Manage your documentation projects and track their status.
            </p>
          </div>
          <button
            onClick={() => setShowDeployModal(true)}
            className="hidden md:flex items-center gap-2 px-3 py-1.5 text-sm font-medium text-black bg-white hover:bg-gray-200 rounded-md transition-colors duration-150"
          >
            <svg
              className="w-4 h-4"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M12 4v16m8-8H4"
              />
            </svg>
            Deploy
          </button>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
          {isLoading ? (
            // Show skeleton cards while loading
            Array.from({ length: 8 }).map((_, index) => (
              <div
                key={`skeleton-${index}`}
                className="animate-fade-in"
                style={{ animationDelay: `${index * 0.05}s` }}
              >
                <SkeletonCard />
              </div>
            ))
          ) : error ? (
            <div className="col-span-full text-center text-red-400 py-12">
              {error}
            </div>
          ) : projects.length === 0 ? (
            <div className="col-span-full text-center text-gray-400 py-12">
              No projects found
            </div>
          ) : (
            // Show actual project cards after loading
            projects.map((p, index) => (
              <div
                key={p}
                className="animate-scale-in opacity-0"
                style={{ animationDelay: `${0.1 + index * 0.05}s` }}
              >
                <ProjectCard project={p} />
              </div>
            ))
          )}
        </div>
      </div>

      <DeployModal isOpen={showDeployModal} onClose={() => setShowDeployModal(false)} />
    </div>
  );
};

export default Dashboard;
