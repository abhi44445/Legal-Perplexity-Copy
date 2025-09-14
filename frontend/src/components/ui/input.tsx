import * as React from "react"
import { cn } from "@/lib/utils"

export interface InputProps
  extends React.InputHTMLAttributes<HTMLInputElement> {}

const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ className, type, ...props }, ref) => {
    return (
      <input
        type={type}
        className={cn(
          "flex h-12 w-full bg-neo-white border-4 border-neo-black px-4 py-3 text-base text-neo-black placeholder:text-neo-gray-500 focus:outline-none focus:ring-3 focus:ring-neo-black focus:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 font-inter transition-all duration-200",
          className
        )}
        ref={ref}
        {...props}
      />
    )
  }
)
Input.displayName = "Input"

export { Input }