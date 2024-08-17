import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import App from "./App";

import { BrowserRouter } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import PageNavbar from "./components/common/PageNavbar";

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <BrowserRouter>
      <AuthProvider>
        <PageNavbar />
        <App />
      </AuthProvider>
    </BrowserRouter>
  </React.StrictMode>
);