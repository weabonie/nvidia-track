import * as React from "react"
import { useParams, Link } from "react-router-dom"

const ProjectDetails = () => {
  const { id } = useParams()

  return (
    <div className="p-6">
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-semibold">Project: {id}</h1>
        <Link to="/projects" className="text-sm text-muted-foreground underline">Back to projects</Link>
      </div>

      <div className="bg-card p-6 rounded-lg">
        <p className="text-sm text-muted-foreground">This is a placeholder project details page for <strong>{id}</strong>. Wire real data here (API fetch) as a next step.</p>
      </div>
    </div>
  )
}

export default ProjectDetails
