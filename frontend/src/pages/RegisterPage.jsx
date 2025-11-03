import { Link } from 'react-router-dom'
import InputField from '../components/InputField'
import AuthContainer from '../components/AuthContainer'

function RegisterPage() {
    return (
        <>
            <AuthContainer>
                <h1 className='text-center mb-4'>
                    Register
                </h1>

                <InputField
                    label="Username"
                    type="text"
                    id="username"
                    placeholder="johndoe"
                />
                <InputField
                    label="Email address"
                    type="text"
                    id="email"
                    placeholder="email@example.com"
                />
                <InputField
                    label="Password"
                    type="password"
                    id="password"
                    placeholder="********"
                />
                <InputField
                    label="Confirm Password"
                    type="password"
                    id="password"
                    placeholder="********"
                />

                <button type="submit" className="btn btn-primary w-100 py-2">Register</button>

                <p className='text-center mt-3'>
                    Already have an account? <Link to="/login" className='text-decoration-none'>Login</Link>
                </p>
            </AuthContainer>
        </>
    )
}

export default RegisterPage
