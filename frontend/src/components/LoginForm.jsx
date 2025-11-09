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
import { Link, useNavigate } from "react-router-dom";
import { useState } from "react";

const LoginForm = () => {
  const [isLoggingIn, setIsLoggingIn] = useState(false);
  const navigate = useNavigate();

  const handleLogin = (e) => {
    e.preventDefault();
    setIsLoggingIn(true);
    
    // Wait for animation to complete before navigating
    setTimeout(() => {
      navigate('/dashboard');
    }, 800);
  };

  return (
    <Card className={`w-100 bg-[#1d1d1d] border-[#7b7b7b] text-white p-6 shadow-lg py-11 transition-all duration-800 ${
      isLoggingIn ? 'opacity-0 scale-95' : 'opacity-100 scale-100'
    }`}>
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
        <button
          onClick={handleLogin}
          className={`bg-nvidia flex justify-center items-center hover:bg-nvidia-hover text-black w-full h-10 font-medium rounded transition-all duration-300 ${
            isLoggingIn ? 'scale-95 opacity-70' : 'scale-100 opacity-100'
          }`}
          disabled={isLoggingIn}
        >
          {isLoggingIn ? (
            <span className="flex items-center gap-2">
              <svg className="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Logging in...
            </span>
          ) : (
            'Login'
          )}
        </button>
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
