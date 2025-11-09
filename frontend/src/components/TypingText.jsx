import React, { useEffect, useState } from "react"

/**
 * TypingText
 * Props:
 * - words: array of strings to cycle through
 * - typingSpeed: ms per character while typing
 * - deletingSpeed: ms per character while deleting
 * - pause: ms to wait after a word finishes typing before deleting
 */
const TypingText = ({
  words = ["Project Management Assistant."],
  typingSpeed = 100,
  deletingSpeed = 50,
  pause = 1400,
  className = "",
}) => {
  const [wordIndex, setWordIndex] = useState(0)
  const [subIndex, setSubIndex] = useState(0)
  const [isDeleting, setIsDeleting] = useState(false)
  const [blink, setBlink] = useState(true)

  // Type / delete effect
  useEffect(() => {
    if (!words || words.length === 0) return

    // When done typing, wait 'pause' then start deleting
    if (!isDeleting && subIndex === words[wordIndex].length) {
      const timeout = setTimeout(() => setIsDeleting(true), pause)
      return () => clearTimeout(timeout)
    }

    // When finished deleting, move to next word after short delay
    if (isDeleting && subIndex === 0) {
      const timeout = setTimeout(() => {
        setIsDeleting(false)
        setWordIndex((w) => (w + 1) % words.length)
      }, 200)
      return () => clearTimeout(timeout)
    }

    const timeout = setTimeout(() => {
      setSubIndex((s) => s + (isDeleting ? -1 : 1))
    }, isDeleting ? deletingSpeed : typingSpeed)

    return () => clearTimeout(timeout)
  }, [subIndex, isDeleting, wordIndex, words, typingSpeed, deletingSpeed, pause])

  // Blinking caret
  useEffect(() => {
    const id = setInterval(() => setBlink((b) => !b), 500)
    return () => clearInterval(id)
  }, [])

  const current = words[wordIndex]?.substring(0, subIndex)

  return (
    <span className={className} aria-live="polite">
      {current}
      <span className={`inline-block ml-1 w-[1px] h-[1.15em] align-middle bg-white ${blink ? "opacity-100" : "opacity-0"}`} />
    </span>
  )
}

export default TypingText
