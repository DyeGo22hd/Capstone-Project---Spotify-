import './navbar.css';
import { useNavigate } from 'react-router-dom';

const Navbar = () => {
    const navigate = useNavigate();

    const navigateToHome = () => {
        Array.from(document.querySelector('ul#navbar').getElementsByTagName('a')).forEach(function (e) {
            e.classList.remove("active")
        });
        document.getElementById('home').className = "active";
        
        navigate('/');
    };

    const navigateToAccount = () => {
        Array.from(document.querySelector('ul#navbar').getElementsByTagName('a')).forEach(function (e) {
            e.classList.remove("active")
        });
        document.getElementById('account').className = "active";

        navigate('/success');
    };

    return (
        <ul id='navbar'>
            <li><a className="active" id='home' onClick={navigateToHome}>HOME</a></li>
            <li><a id='account' onClick={navigateToAccount}>ACCOUNT</a></li>
        </ul>
    )
};

export default Navbar;