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
    navigate(`/projects/${id}`)
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
              <Button asChild size="sm" variant="outline">
                <a href={link} target="_blank" rel="noreferrer" onClick={(e)=>e.stopPropagation()}>View</a>
              </Button>
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
        <div className="flex items-center gap-2">
          <Button className="text-white" variant="link" size="sm" onClick={(e)=>{e.stopPropagation(); navigate(`/projects/${project.id ?? name.replace(/\s+/g,'-').toLowerCase()}/settings`)}}>Settings</Button>
        </div>
      </CardFooter>
    </Card>
  )
}

export default ProjectCard
