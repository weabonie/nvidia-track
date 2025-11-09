import Navbar from './components/Navbar';
import Footer from './components/Footer';
import { Outlet } from 'react-router-dom';

const Layout = ({children}) => {
    return (
        <div className="flex flex-col min-h-svh w-full"> 
            <Navbar />
            <main className="flex-grow">
                <Outlet/>
            </main>
            <Footer />
        </div>
    )
}

export default Layout;