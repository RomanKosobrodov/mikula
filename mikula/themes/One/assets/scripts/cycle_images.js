var current = 0;

function cycle_images(image_list) {
    let images = image_list;
    const length = image_list.length;
    return (e) => {
       current = (current + 1) % length;
       e.target.src = images[current];
    }
}