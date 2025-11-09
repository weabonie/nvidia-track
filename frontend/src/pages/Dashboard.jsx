import * as React from "react"
import { useState, useEffect } from "react"
import ProjectCard from "../components/ProjectCard"

const sampleProjects = [
    {
        id: 1,
        name: "nvidia-track-frontend",
        description: "Frontend for the NVIDIA tracking app. Shows projects, dashboards, and auth.",
        updatedAt: "2 days ago",
        link: "#",
        tech: ["React", "Vite", "Tailwind"],
        visibility: "public",
    },
    {
        id: 2,
        name: "nvidia-track-backend",
        description: "API and ingestion pipeline for telemetry and project data.",
        updatedAt: "6 days ago",
        link: "#",
        tech: ["Node", "Express", "Postgres"],
        visibility: "private",
    },
    {
        id: 3,
        name: "model-eval",
        description: "Model evaluation tooling and training job visualizer.",
        updatedAt: "3 hours ago",
        link: "#",
        tech: ["Python", "FastAPI", "Docker"],
        visibility: "public",
    },
    {
        id: 4,
        name: "infra",
        description: "IaC for deploying preview environments and infra monitoring.",
        updatedAt: "1 month ago",
        link: "#",
        tech: ["Terraform", "AWS"],
        visibility: "private",
    },
    {
        id: 5,
        name: "examples",
        description: "Sample apps and integration examples for the SDK.",
        updatedAt: "yesterday",
        link: "#",
        tech: ["React", "Typescript"],
        visibility: "public",
    },
    {
        id: 6,
        name: "design-system",
        description: "Shared components, tokens, and utilities used across apps.",
        updatedAt: "3 weeks ago",
        link: "#",
        tech: ["Storybook", "Tailwind"],
        visibility: "private",
    },
    {
        id: 7,
        name: "data-warehouse",
        description: "ETL jobs and analytics dashboards for product telemetry.",
        updatedAt: "4 days ago",
        link: "#",
        tech: ["Airflow", "BigQuery"],
        visibility: "private",
    },
    {
        id: 8,
        name: "cli-tool",
        description: "CLI utilities for developers to scaffold projects and run tasks.",
        updatedAt: "2 hours ago",
        link: "#",
        tech: ["Go"],
        visibility: "public",
    },
]

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
    )
}

const Dashboard = () => {
    const [isLoading, setIsLoading] = useState(true)

    useEffect(() => {
        // Simulate loading delay
        const timer = setTimeout(() => {
            setIsLoading(false)
        }, 1200) // 1.2 seconds loading

        return () => clearTimeout(timer)
    }, [])

    return (
        <div className="p-12 animate-fade-in">
            <div className="flex items-center justify-between mb-6 animate-slide-down opacity-0" style={{ animationDelay: "0.1s" }}>
                <h1 className="text-2xl text-nvidia font-semibold">Projects</h1>
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
                ) : (
                    // Show actual project cards after loading
                    sampleProjects.map((p, index) => (
                        <div 
                            key={p.id} 
                            className="animate-scale-in opacity-0" 
                            style={{ animationDelay: `${0.1 + (index * 0.05)}s` }}
                        >
                            <ProjectCard project={p} />
                        </div>
                    ))
                )}
            </div>
        </div>
    )
}

export default Dashboard;