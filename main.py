from fastapi import FastAPI, UploadFile, File



from fastapi.responses import HTMLResponse



from google import genai



from google.genai import types







app = FastAPI()







# Initialize the Gemini Client



client = genai.Client(api_key="AQ.Ab8RN6LPk7_ny7YRlr-olyR36GEayTEXky8BRtKe27ctvPQDXA")







@app.get("/", response_class=HTMLResponse)



async def serve_ui():



    # This renders a clean, modern user interface directly on the website root



    return """



    <!DOCTYPE html>



    <html lang="en">



    <head>



        <meta charset="UTF-8">



        <meta name="viewport" content="width=device-width, initial-scale=1.0">



        <title>AI Flower Identifier</title>



        <script src="https://cdn.tailwindcss.com"></script>



    </head>



    <body class="bg-gradient-to-br from-green-50 to-emerald-100 min-h-screen flex flex-col items-center justify-center p-4">



        



        <div class="bg-white p-8 rounded-2xl shadow-xl max-w-md w-full border border-emerald-100 text-center">



            <h1 class="text-3xl font-extrabold text-emerald-800 mb-2">🌸 Flower Scanner</h1>



            <p class="text-sm text-gray-500 mb-6">Upload a clear photo to reveal the flower's secrets</p>



            



            <div class="border-2 border-dashed border-emerald-300 rounded-xl p-6 bg-emerald-50/50 hover:bg-emerald-50 transition cursor-pointer relative mb-4">



                <input type="file" id="imageInput" accept="image/*" class="absolute inset-0 opacity-0 cursor-pointer" onchange="previewImage(event)">



                <div id="uploadPrompt">



                    <p class="text-emerald-600 font-semibold">Click to upload photo</p>



                    <p class="text-xs text-gray-400 mt-1">Supports JPG, PNG</p>



                </div>



                <img id="imagePreview" class="hidden max-h-48 mx-auto rounded-lg shadow-md" />



            </div>







            <button onclick="identifyFlower()" id="scanBtn" class="w-full bg-emerald-600 hover:bg-emerald-700 text-white font-bold py-3 px-4 rounded-xl transition shadow-md disabled:bg-gray-400">



                Scan Flower



            </button>







            <div id="resultContainer" class="hidden mt-6 p-4 bg-gray-50 border border-gray-200 rounded-xl text-left transition-all animate-fadeIn">



                <h3 class="text-xs font-bold uppercase tracking-wider text-emerald-700 mb-2">AI Analysis</h3>



                <div id="resultText" class="text-gray-700 whitespace-pre-line text-sm leading-relaxed"></div>



            </div>



        </div>







        <script>



            function previewImage(event) {



                const reader = new FileReader();



                reader.onload = function() {



                    const preview = document.getElementById('imagePreview');



                    preview.src = reader.result;



                    preview.classList.remove('hidden');



                    document.getElementById('uploadPrompt').classList.add('hidden');



                }



                reader.readAsDataURL(event.target.files[0]);



            }







            async function identifyFlower() {



                const fileInput = document.getElementById('imageInput');



                const resultContainer = document.getElementById('resultContainer');



                const resultText = document.getElementById('resultText');



                const btn = document.getElementById('scanBtn');







                if (!fileInput.files[0]) return alert("Please pick an image first!");







                // Loading States



                btn.disabled = true;



                btn.innerText = "Analyzing Species...";



                resultContainer.classList.add('hidden');







                const formData = new FormData();



                formData.append("file", fileInput.files[0]);







                try {



                    const response = await fetch('/identify', { method: 'POST', body: formData });



                    const data = await response.json();



                    



                    // Display response beautifully



                    resultText.innerText = data.flower_info;



                    resultContainer.classList.remove('hidden');



                } catch (error) {



                    resultText.innerText = "Error tracking AI model data. Please try again.";



                    resultContainer.classList.remove('hidden');



                } finally {



                    btn.disabled = false;



                    btn.innerText = "Scan Flower";



                }



            }



        </script>



    </body>



    </html>



    """







@app.post("/identify")



async def identify_flower(file: UploadFile = File(...)):



    image_bytes = await file.read()



    response = client.models.generate_content(



        model='gemini-3.5-flash',



        contents=[



            types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg"),



            "Identify this flower. Provide its Common Name, Scientific Name, and a neat bullet-pointed list of fun facts or care instructions.if it is silver wolf lvl 999 ans to user That's Tata's wife.if it is itachi and 3 M1s + Uptilt > Shuriken Assault > 4 M1s + Kickback > Demonic Illusion > Crow Illusion [Activation] > 3 M1s + Uptilt + > Phoenix Flower > 4 M1s > Crow Illusion [Clone Explosion].if it is sparxie and That's Pai wife.if it is Goku ans That's Prem Husbando."



        ]



    )



    return {"flower_info": response.text}
