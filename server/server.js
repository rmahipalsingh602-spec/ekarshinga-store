https://github.com/rmahipalsingh602-spec/ekarshinga-store/tree/main/server/server
import express from "express";
import cors from "cors";
import dotenv from "dotenv";
import uploadRoutes from "./routes/uploadRoutes.js";
import assetRoutes from "./routes/assetRoutes.js";
import gameRoutes from "./routes/gameRoutes.js";
import adminRoutes from "./routes/adminRoutes.js";

dotenv.config();

const app = express();
const PORT = process.env.PORT || 5000;

app.use(cors());
app.use(express.json());
app.use("/uploads", express.static("uploads"));

// Routes
app.use("/api/upload", uploadRoutes);
app.use("/api/assets", assetRoutes);
app.use("/api/games", gameRoutes);
app.use("/api/admin", adminRoutes);

app.get("/", (req, res) => {
  res.send("Ekarshinga Backend is Running 🚀");
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
