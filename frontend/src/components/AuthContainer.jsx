function AuthContainer({ children }) {
    return (
        <div className="container d-flex justify-content-center align-items-center ">
            <div className="card p-4" style={{ maxWidth: '500px', width: '100%' }}>
                {children}
            </div>
        </div>
    )
}

export default AuthContainer
