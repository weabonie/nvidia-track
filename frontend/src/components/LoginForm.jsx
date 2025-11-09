import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";

import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardAction,
  CardFooter,
  CardTitle,
} from "@/components/ui/card";

import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { Link } from "react-router-dom";

const LoginForm = () => {
  return (
    <Card className="w-100 bg-[#1d1d1d] border-[#7b7b7b] text-white p-6 shadow-lg py-11">
      <CardHeader className="text-center">
        <CardTitle className="text-2xl font-medium">Login to your account</CardTitle>
        {/* <CardDescription>
          Enter your email below to login to your account
        </CardDescription> */}
        {/* <CardAction>
          <Button variant="link">Sign Up</Button>
        </CardAction> */}
      </CardHeader>
      <CardContent>
        <form>
          <div className="flex flex-col gap-6">
            <div className="grid gap-2">
              <Label htmlFor="email">Email</Label>
              <Input
                id="email"
                type="email"
                className="bg-[#171717] rounded-sm"
                // placeholder="m@example.com"  
                required
              />
            </div>
            <div className="grid gap-2">
              <div className="flex items-center">
                <Label htmlFor="password">Password</Label>
                <a
                  href="#"
                  className="text-nvidia ml-auto inline-block text-sm underline-offset-4 hover:underline"
                >
                  Forgot your password?
                </a>
              </div>
              <Input id="password" type="password" className="bg-[#171717] rounded-sm" required />
            </div>
          </div>
        </form>
      </CardContent>
      <CardFooter className="flex-col gap-4">
        <Link to="/projects" className="bg-nvidia flex justify-center items-center hover:bg-nvidia-hover text-black w-full h-10">
          Login
        </Link>
        {/* <Button variant="outline" className="w-full">
          Login with Google
        </Button> */}

        <span className="mr-auto inline-block">
          Don't have an account?{" "}
          <a
            href="#"
            className="font-medium text-nvidia underline-offset-4 hover:underline"
          >
            Register
          </a>
        </span>
      </CardFooter>
    </Card>
  );
};

export default LoginForm;
