const letters_string = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789~!@#$%^&*()_+`-={}|[]\\:\";\'<>?,./";
const letters_array = letters_string.split("");

const password_input = document.getElementsByClassName("Password_Display")[0]

console.log(letters_array);

function getRandomItem(arr) {
    const randomIndex = Math.floor(Math.random() * arr.length);
    return arr[randomIndex];
}

function onClick(){
    var password = "";

    for(let i = 0; i < 16; i++){
        let letter = getRandomItem(letters_array);

        password += letter

    };

    console.log("Ran: " + password)

    password_input.value = password

    navigator.clipboard.writeText(password)

};