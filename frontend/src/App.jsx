import './App.css'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import RegisterPage from './pages/RegisterPage'
import LoginPage from './pages/LoginPage'

function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path='/Register' element={<RegisterPage />} />
                <Route path='/Login' element={<LoginPage />} />
            </Routes>
        </BrowserRouter>
    )
}

export default App
