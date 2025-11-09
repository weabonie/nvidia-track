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

// import Login from './pages/auth/Login';
// import Register from './pages/auth/Register';
// import Header from './components/nav/Header';

const router = createBrowserRouter([
  {
    path: "/",
    element: <Layout />,
    children: [
      {
        index: true, // This makes Home the default child route for '/'
        element: <Home />,
      },
      // {
      //   path: 'about',
      //   element: <About />,
      // },
      // {
      //   path: 'contact',
      //   element: <Contact />,
      // },
    ],
  },
  // You can add other top-level routes without the main layout here if needed
  {
    path: '/login',
    element: <LoginPage />,
  },

   {
    path: "/projects",
    element: <Layout />,
    children: [
      {
        index: true, // This makes Home the default child route for '/'
        element: <Home />,
      },
      // {
      //   path: 'about',
      //   element: <About />,
      // },
      // {
      //   path: 'contact',
      //   element: <Contact />,
      // },
    ],
  },
]);

function App({ routes }) {
  return (
    <>
      <RouterProvider router={router} />
    </>
  );
}

export default App;
