function like(postId) {
    const likeCount = document.getElementById(`likes-count-${postId}`);
    const likeButton = document.getElementById(`like-button-${postId}`);

    fetch("/like-post/" + {postId}, { method: "POST" })
    .then((res) => res.json())
    .then((data) => console.log(data));
    //{
    //     likeCount.innerHTML = data["likes"];
    //     if (data["liked"] === true ) {
    //         likeButton.className = "fa-solid fa-thumbs-up";
    //     } else {
    //         likeButton.className = "fa-regular fa-thumbs-up";}
    //}).catch((e) => alert("Could not like post."));
    console.log(likeCount.value);
}