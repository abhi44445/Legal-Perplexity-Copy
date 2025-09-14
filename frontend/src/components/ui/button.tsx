import * as React from "react"
import { Slot } from "@radix-ui/react-slot"
import { cva, type VariantProps } from "class-variance-authority"
import { cn } from "@/lib/utils"

const buttonVariants = cva(
  "inline-flex items-center justify-center gap-2 whitespace-nowrap text-sm font-bold transition-all disabled:pointer-events-none disabled:opacity-50 [&_svg]:pointer-events-none [&_svg:not([class*='size-'])]:size-4 shrink-0 [&_svg]:shrink-0 outline-none focus-visible:outline-3 focus-visible:outline-offset-2 focus-visible:outline-neo-black border-4 border-neo-black font-inter",
  {
    variants: {
      variant: {
        default:
          "bg-neo-black text-neo-white hover:bg-neo-white hover:text-neo-black transform-gpu hover:translate-x-1 hover:translate-y-1 shadow-neo hover:shadow-none active:translate-x-2 active:translate-y-2 active:shadow-none",
        outline:
          "bg-neo-white text-neo-black hover:bg-neo-black hover:text-neo-white transform-gpu hover:translate-x-1 hover:translate-y-1 shadow-neo hover:shadow-none active:translate-x-2 active:translate-y-2 active:shadow-none",
        ghost:
          "border-transparent bg-transparent text-neo-black hover:bg-neo-black hover:text-neo-white hover:border-neo-black",
        destructive:
          "bg-red-600 text-neo-white border-red-600 hover:bg-neo-white hover:text-red-600 transform-gpu hover:translate-x-1 hover:translate-y-1 shadow-neo hover:shadow-none",
      },
      size: {
        default: "h-12 px-6 py-3",
        sm: "h-10 px-4 py-2 text-sm",
        lg: "h-14 px-8 py-4 text-base",
        icon: "h-12 w-12",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
)

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, asChild = false, ...props }, ref) => {
    const Comp = asChild ? Slot : "button"
    return (
      <Comp
        className={cn(buttonVariants({ variant, size, className }))}
        ref={ref}
        {...props}
      />
    )
  }
)
Button.displayName = "Button"

export { Button, buttonVariants }