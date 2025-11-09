import * as React from "react"
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

const Dashboard = () => {
    return (
        <div className="p-12">
            <div className="flex items-center justify-between mb-6">
                <h1 className="text-2xl text-nvidia font-semibold">Projects</h1>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
                {sampleProjects.map((p) => (
                    <ProjectCard key={p.id} project={p} />
                ))}
            </div>
        </div>
    )
}

export default Dashboard;