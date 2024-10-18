const net = require("net");

async function rpcCall(id, method, params) {
  return new Promise((resolve, reject) => {
    const client = new net.Socket();
    const request = {
      id,
      method,
      params,
    };
    client.connect(8080, "localhost", () => {
      console.log("Connected");
      client.write(JSON.stringify(request));
    });

    client.on("data", (data) => {
      console.log("Received: " + data);
      resolve(JSON.parse(data));
      client.destroy();
    });

    client.on("close", () => {
      console.log("Connection closed");
      reject("Connection closed");
    });
  });
}

async function main() {
  try {
    const floor_result = await rpcCall("1", "floor", [1.1]);
    console.log(floor_result);
    const nroot_result = await rpcCall("2", "nroot", [2, 2]);
    console.log(nroot_result);
    const reverse_result = await rpcCall("3", "reverse", ["hello"]);
    console.log(reverse_result);
    const validAnagram_result = await rpcCall("4", "validAnagram", [
      "hello",
      "llohe",
    ]);
    console.log(validAnagram_result);
    const sort_result = await rpcCall("5", "sort", [[3, 2, 1]]);
    console.log(sort_result);
  } catch (error) {
    console.error(error);
  }
}

main();
