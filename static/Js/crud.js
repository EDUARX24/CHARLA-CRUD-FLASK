document.addEventListener('DOMContentLoaded', () => {
    const forms = document.querySelectorAll('.form-eliminar');
  
    forms.forEach(form => {
      form.addEventListener('submit', function (e) {
        e.preventDefault(); // Detiene el envío por defecto
  
        const nombre = form.getAttribute('data-nombre');
        const cargo = form.getAttribute('data-cargo');
  
        Swal.fire({
          title: '¿Estás seguro?',
          html: `¿Deseas eliminar al empleado <strong>${nombre}</strong> (<em>${cargo}</em>)?`,
          icon: 'warning',
          showCancelButton: true,
          confirmButtonColor: '#d33',
          cancelButtonColor: '#6c757d',
          confirmButtonText: 'Sí, eliminar',
          cancelButtonText: 'Cancelar'
        }).then((result) => {
          if (result.isConfirmed) {
            form.submit();
          }
        });
      });
    });
  });
  