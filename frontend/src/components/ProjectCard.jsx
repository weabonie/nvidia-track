import * as React from "react"
import { useNavigate } from "react-router-dom"

import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardAction,
  CardContent,
  CardFooter,
} from "./ui/card"

import { Button } from "./ui/button"

const ProjectCard = ({ project = {} }) => {
  const {
    name = "Untitled Project",
    description = "No description provided",
    updatedAt = "—",
    link = "#",
    tech = [],
    visibility = "private",
  } = project

  const navigate = useNavigate()

  const handleNavigate = () => {
    const id = project.id ?? name.replace(/\s+/g, "-").toLowerCase()
    navigate(`/dashboard/projects/${id}`)
  }

  return (
    <Card
      role="button"
      tabIndex={0}
      onClick={handleNavigate}
      onKeyDown={(e) => {
        if (e.key === "Enter" || e.key === " ") {
          e.preventDefault()
          handleNavigate()
        }
      }}
      className="min-h-[100px] border-[#363636]! rounded-sm p-6 bg-[#0a0a0a] flex flex-col justify-between cursor-pointer transition-colors duration-150 hover:border-white! focus:border-white"
    >
      <div>
        <CardHeader className="p-0">
          <div className="flex items-start gap-3 w-full">
            <div className="flex-1">
              <CardTitle className="text-lg text-nvidia">{name}</CardTitle>
              <CardDescription className="line-clamp-2 text-sm text-white">{description}</CardDescription>
            </div>
            <CardAction>
              <button 
                onClick={(e) => {
                  e.stopPropagation();
                  navigate(`/dashboard/projects/${project.id ?? name.replace(/\s+/g,'-').toLowerCase()}/settings`);
                }}
                className="text-gray-400 hover:text-white transition-colors"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
              </button>
            </CardAction>
          </div>
        </CardHeader>

        <CardContent className="p-0 pt-4">
          <div className="flex flex-wrap gap-2">
            {tech.map((t) => (
              <span key={t} className="bg-[#363636]! text-white text-xs px-2 py-1 rounded bg-muted text-muted-foreground">{t}</span>
            ))}
          </div>
        </CardContent>
      </div>

      <CardFooter className="p-0 justify-between">
        <div className="text-xs text-muted-foreground">Updated {updatedAt}</div>
      </CardFooter>
    </Card>
  )
}

export default ProjectCard
