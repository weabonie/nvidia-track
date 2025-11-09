import React from "react";
import {
  Route,
  createBrowserRouter,
  createRoutesFromElements,
  RouterProvider,
} from "react-router-dom";

import Home from "./pages/Home";
import Layout from './components/Layout'
import LoginPage from './pages/LoginPage'
import Dashboard from "./pages/Dashboard";
import ProjectLayout from "./components/ProjectsLayout";
import ProjectDetails from "./pages/ProjectDetails";
import ProjectOverview from "./pages/ProjectOverviewFixed";

// import Login from './pages/auth/Login';
// import Register from './pages/auth/Register';
// import Header from './components/nav/Header';

const router = createBrowserRouter([
  {
    path: "/",
    element: <Layout />,
    children: [
      {
        index: true,
        element: <Home />,
      }
    ],
  },
  {
    path: '/login',
    element: <LoginPage />,
  },
  {
    path: "/dashboard",
    element: <ProjectLayout />,
    children: [
      {
        index: true,
        element: <Dashboard />,
      },
      {
        path: "projects/:id/*",
        element: <ProjectDetails />,
      },
      {
        path: "templates",
        element: <div className="p-8 text-white">Templates Coming Soon</div>,
      },
      {
        path: "team",
        element: <div className="p-8 text-white">Team Management Coming Soon</div>,
      },
      {
        path: "integrations",
        element: <div className="p-0"><React.Suspense fallback={<div className='p-8 text-white'>Loading Integrations...</div>}><IntegrationsLazy /></React.Suspense></div>,
      },
    ],
  },
]);
const IntegrationsLazy = React.lazy(() => import('./pages/Integrations'));

function App({ routes }) {
  return (
    <>
      <RouterProvider router={router} />
    </>
  );
}

export default App;
