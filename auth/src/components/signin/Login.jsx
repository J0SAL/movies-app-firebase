import React, { useState } from "react";
import { auth, provider } from "../../utils/firebase";
import {
    signInWithPopup,
    signInWithEmailAndPassword,
} from "firebase/auth";

import { useAuth } from "../../context/AuthContext";

var default_user = {
    email: "",
    password: "",
};
function Login() {
    const [user, setUser] = useState(default_user);

    const handleChange = (e) => {
        setUser({ ...user, [e.target.name]: e.target.value });
    };

    const { login, logout } = useAuth();

    const signIn = async (e) => {
        e.preventDefault();
        setUser(default_user);
        try {
            let result = await signInWithEmailAndPassword(
                auth,
                user.email,
                user.password
            );
            const email = result.user.email;
            const firebaseIdToken = await result.user.getIdToken();
            console.log(email);
            console.log(firebaseIdToken);
            login(firebaseIdToken);
        } catch (error) {
            console.log(error);
        }
    };

    const signInGoogle = async () => {
        try {
            let result = await signInWithPopup(auth, provider);
            const email = result.user.email;
            const idToken = await result.user.getIdToken();
            console.log(email);
            console.log(idToken);
            login(idToken);
        } catch (error) {
            console.log(error);
        }
    };



    return (
        <div>
            <h2>Login</h2>
            <form onSubmit={signIn}>
                <div
                    style={{
                        display: "flex",
                        flexDirection: "column",
                        minWidth: "25vw",
                        width: "25vw",
                    }}
                >
                    Email{" "}
                    <input
                        type="email"
                        name="email"
                        value={user.email}
                        onChange={handleChange}
                    />
                    Password{" "}
                    <input
                        type="password"
                        name="password"
                        value={user.password}
                        onChange={handleChange}
                    />
                    <button type="submit">Submit</button>
                    <button type="button" onClick={signInGoogle}>
                        Google
                    </button>
                    <button type="button" onClick={logout}>
                        Logout
                    </button>
                </div>
            </form>
        </div>
    );
}

export default Login;