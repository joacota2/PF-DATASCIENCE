function helpful(review_id) {
	const helpfulCount = document.getElementById(`helpful-${review_id}`);
	const helpfulButton = document.getElementById(`helpful-button-${review_id}`);

	fetch(`/vote_helpful/${review_id}`, { method: "POST" })
		.then((res) => res.json())
		.then((data) => {
			helpfulCount.innerHTML = data["votes"];
			if (data["voted"] === true) {
				helpfulButton.className = "card-link btn btn-success";
			} else {
				helpfulButton.className = "card-link btn btn-outline-success";
			}
		})
		.catch((e) => alert(e));
}
function nothelpful(review_id) {
	const notHelpfulCount = document.getElementById(`unhelpful-${review_id}`);
	const notHelpfulButton = document.getElementById(
		`unhelpful-button-${review_id}`
	);

	fetch(`/vote_unhelpful/${review_id}`, { method: "POST" })
		.then((res) => res.json())
		.then((data) => {
			notHelpfulCount.innerHTML = data["votes"];
			if (data["voted"] === true) {
				notHelpfulButton.className = "card-link btn btn-danger";
			} else {
				notHelpfulButton.className = "card-link btn btn-outline-danger";
			}
		})
		.catch((e) => alert(e));
}
function add2favs(asin) {
	const favButton = document.getElementById(`fav-button-${asin}`);

	fetch(`/add2favs/${asin}`, { method: "POST" })
		.then((res) => res.json())
		.then((data) => {
			if (data["in_favs"] === true) {
				favButton.className = "btn btn-sm btn-danger";
				favButton.innerHTML = "Remove from favorites";
				console.log(`${asin} added to favorites`);
			} else {
				favButton.className = "btn btn-sm btn-outline-warning";
				favButton.innerHTML = "Add to favorites";
				console.log(`${asin} removed from favorites`);
			}
		})
		.catch((e) => console.log(e));
}
function add2cart(asin) {
	const cartButton = document.getElementById(`cart-button-${asin}`);

	fetch(`/add2cart/${asin}`, { method: "POST" })
		.then((res) => res.json())
		.then((data) => {
			if (data["in_cart"] === true) {
				cartButton.className = "btn btn-sm btn-dark";
				cartButton.innerHTML = "Remove from cart";
				console.log(`${asin} added to cart`);
			} else {
				cartButton.className = "btn btn-sm btn-outline-dark";
				cartButton.innerHTML = "Add to cart";
				console.log(`${asin} removed from cart`);
			}
		})
		.catch((e) => console.log(e));
}
