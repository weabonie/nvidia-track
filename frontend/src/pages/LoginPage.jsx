import LoginForm from "../components/LoginForm";

const LoginPage = () => {
  return (
    <div className="w-full h-full">
      <div className="w-1/2 min-h-svh bg-black flex flex-col justify-center items-center">
        <div>
            <LoginForm/>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;
