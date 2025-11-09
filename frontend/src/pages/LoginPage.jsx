import LoginForm from "../components/LoginForm";

const LoginPage = () => {
  return (
    <div className="w-full h-full">
      <div className="bg-gradient-to-b from-lime-900 to-zinc-900 to-lime-800 w-1/2 min-h-svh bg-black flex flex-col justify-center items-center">
        <div>
            <LoginForm/>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;
