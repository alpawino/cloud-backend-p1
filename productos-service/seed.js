const mongoose = require("mongoose");

const mongoURI = process.env.MONGO_URI || "mongodb://172.31.82.16:27017/productsDB";
mongoose.connect(mongoURI)
  .then(() => console.log("Mongo conectado para Sembrar 😼"))
  .catch(err => {
    console.log("Error conectando a Mongo:", err);
    process.exit(1);
  });

const ProductSchema = new mongoose.Schema({
  name: String,
  price: Number,
  stock: Number,
  category: String
});

const Product = mongoose.model("Product", ProductSchema);

const generateProducts = async () => {
  try {
    // 🧹 Limpia la colección antes de insertar
    await Product.deleteMany({});
    console.log("🧹 Colección limpiada");

    const products = [];

    for (let i = 0; i < 20000; i++) {
      products.push({
        name: "Producto " + i,
        price: Math.floor(Math.random() * 1000) + 1,
        stock: Math.floor(Math.random() * 100),
        category: ["Electrónica", "Ropa", "Hogar"][Math.floor(Math.random() * 3)]
      });
    }

    const BATCH_SIZE = 1000;
    for (let i = 0; i < products.length; i += BATCH_SIZE) {
      const batch = products.slice(i, i + BATCH_SIZE);
      await Product.insertMany(batch, { ordered: false });
      console.log(`✅ Insertados ${Math.min(i + BATCH_SIZE, products.length)} / 20000`);
    }

    console.log("🐾 20,000 productos insertados 😼");
  } catch (error) {
    console.error("❌ Error insertando productos:", error.message);
  } finally {
    mongoose.connection.close();
    console.log("🔌 Conexión cerrada");
  }
};

// Espera a que Mongo esté conectado antes de correr
mongoose.connection.once("open", () => {
  console.log("🚀 Conexión lista, iniciando seed...");
  generateProducts();
});