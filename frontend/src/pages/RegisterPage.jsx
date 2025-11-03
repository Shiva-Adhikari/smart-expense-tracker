import { Link } from 'react-router-dom'

function RegisterPage() {
    return (
        <>
        <div className="container d-flex justify-content-center align-items-center ">
            <div className="card p-4" style={{ maxWidth: '500px', width: '100%' }}>
            <h1 className='text-center mb-4'>
                Register
            </h1>

            <div className="mb-3">
                <label htmlFor="username" className="form-label d-block text-start">Username</label>
                <input type="text" className="form-control" id="username" placeholder='johndoe'/>
            </div>
            <div className="mb-3">
                <label htmlFor="email" className="form-label d-block text-start">Email address</label>
                <input type="email" className="form-control" id="email" placeholder="email@example.com" />
            </div>
            <div className="mb-3">
                <label htmlFor="password" className="form-label d-block text-start">Password</label>
                <input type="password" className="form-control" id="password" placeholder="********" />
            </div>
            <div className="mb-3">
                <label htmlFor="confirmPassword" className="form-label d-block text-start">Confirm Password</label>
                <input type="password" className="form-control" id="confirmPassword" placeholder="********" />
            </div>
            <button type="submit" className="btn btn-primary w-100 py-3">Register</button>

            <p className='text-center mt-3'>
                Already have an account? <Link to="/login" className='text-decoration-none'>Login</Link>
            </p>
            </div>
        </div>
    </>
    )
}

export default RegisterPage
