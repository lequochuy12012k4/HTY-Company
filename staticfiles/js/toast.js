
function showToast(message, status = 'success') {
    const toast = document.createElement('div');
    const toastId = 'toast-' + Date.now();
    toast.id = toastId;

    const statusClasses = status === 'success'
        ? 'bg-green-100 text-green-800 font-bold'
        : (status === 'error' ? 'bg-red-100 text-red-800' : 'bg-blue-100 text-blue-800');

    toast.className = `fixed top-5 right-5 p-4 rounded-lg shadow-lg flex items-center justify-between max-w-xs sm:max-w-sm z-50 ${statusClasses}`;
    toast.setAttribute('role', 'alert');

    toast.innerHTML = `
        <span class="font-medium">${message}</span>
        <button type="button" class="ml-4 -mx-1.5 -my-1.5 bg-transparent rounded-lg focus:ring-2 focus:ring-gray-300 p-1.5 hover:bg-gray-200 inline-flex h-8 w-8" aria-label="Close">
            <span class="sr-only">Close</span>
            <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"></path></svg>
        </button>
    `;

    document.body.appendChild(toast);

    const closeButton = toast.querySelector('button');
    closeButton.onclick = () => {
        toast.remove();
    };

    setTimeout(() => {
        const activeToast = document.getElementById(toastId);
        if (activeToast) {
            activeToast.remove();
        }
    }, 5000);
}
