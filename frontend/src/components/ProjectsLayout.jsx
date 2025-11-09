import Navbar from './Navbar';
import Footer from './Footer';
import { Outlet } from 'react-router-dom';

const ProjectLayout = ({children}) => {
    return (
        <div className="flex flex-col min-h-svh w-full"> 

            <main className="flex-grow">
                <Outlet/>
            </main>

        </div>
    )
}

export default ProjectLayout;