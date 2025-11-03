import { Link } from 'react-router-dom'
import AuthContainer from '../components/AuthContainer'
import InputField from '../components/InputField'

function LoginPage() {
    return (
        <>
            <AuthContainer>
                <h1 className='text-center mb-4'>
                    Login
                </h1>

                <InputField
                    label="Username"
                    type="text"
                    id="username"
                    placeholder="johndoe"
                />
                <InputField
                    label="Password"
                    type="password"
                    id="password"
                    placeholder="********"
                />
                <button className='btn btn-primary w-100 py-2'>Login</button>

                <p className='text-center mt-3'>
                    Don't have an account? <Link to="/register" className='text-decoration-none'>Register</Link>
                </p>
            </AuthContainer>
        </>
    )
}

export default LoginPage
