import LoginForm from "../components/LoginForm";

const LoginPage = () => {
  return (
    <div className="w-full h-full animate-fade-in">
      <div className="bg-gradient-to-b from-lime-900 to-zinc-900 to-lime-800 w-1/2 min-h-svh bg-black flex flex-col justify-center items-center">
        <div className="animate-scale-in opacity-0" style={{ animationDelay: "0.3s" }}>
            <LoginForm/>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;
