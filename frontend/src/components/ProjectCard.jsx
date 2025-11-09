import * as React from "react"
import { useEffect, useMemo, useState } from "react"
import axios from "axios"
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

// ProjectCard can accept either a projectName string or a project object
const ProjectCard = ({ projectName, project }) => {
  console.log(projectName);

  const navigate = useNavigate()

  // Derive display name from provided props
  const displayName = useMemo(() => (projectName || project?.name || "Untitled Project"), [projectName, project])

  // Slugs for API and routing
  const apiName = useMemo(() => displayName.trim().toLowerCase().replace(/\s+/g, ""), [displayName]) // remove spaces for API (e.g., "UH Events" -> "uhevents")
  const routeSlug = useMemo(() => displayName.trim().toLowerCase().replace(/\s+/g, "-"), [displayName])

  // Local state for fetched repo info
  const [details, setDetails] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  useEffect(() => {
    let cancelled = false
    const controller = new AbortController()
    const fetchDetails = async () => {
      if (!apiName) return
      try {
        setLoading(true)
        setError(null)
        const resp = await axios.get("https://apihackutd.siru.dev/repo", {
          params: { name: apiName },
          signal: controller.signal,
        })
        if (!cancelled) setDetails(resp.data)
      } catch (e) {
        if (!cancelled) setError(e?.message || "Failed to load repo info")
      } finally {
        if (!cancelled) setLoading(false)
      }
    }
    fetchDetails()
    return () => {
      cancelled = true
      try { controller.abort() } catch {}
    }
  }, [apiName])

  const handleNavigate = () => {
    const id = project?.id ?? routeSlug
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
              <CardTitle className="text-lg text-nvidia">{displayName}</CardTitle>
              <CardDescription className="line-clamp-2 text-sm text-white">
                {loading && (
                  <span className="text-gray-400">Loading repository details…</span>
                )}
                {!loading && (details?.goal || project?.description || "No description provided")}
              </CardDescription>
            </div>
            <CardAction>
              <button 
                onClick={(e) => {
                  e.stopPropagation();
                  navigate(`/dashboard/projects/${project?.id ?? routeSlug}/settings`);
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
            {loading && (
              <span className="bg-[#363636]! text-gray-300 text-xs px-2 py-1 rounded">Loading…</span>
            )}
            {!loading && details?.dependencies?.length > 0 && details.dependencies.slice(0, 4).map((t) => (
              <span key={t} className="bg-[#363636]! text-white text-xs px-2 py-1 rounded">{t}</span>
            ))}
            {!loading && details?.doc_generation?.response?.url && (
              <a
                href={details.doc_generation.response.url}
                target="_blank"
                rel="noreferrer"
                onClick={(e)=> e.stopPropagation()}
                className="text-xs px-2 py-1 rounded bg-[#76B900]/15 text-[#76B900] border border-[#76B900]/30 hover:bg-[#76B900]/25 transition"
              >
                Docs
              </a>
            )}
          </div>
        </CardContent>
      </div>

      <CardFooter className="p-0 justify-between">
        <div className="text-xs text-muted-foreground">
          {details?.doc_generation?.status ? (
            <span className="text-gray-400">Status: {details.doc_generation.status}</span>
          ) : (
            <span className="text-gray-500">Ready</span>
          )}
        </div>
      </CardFooter>
    </Card>
  )
}

export default ProjectCard
