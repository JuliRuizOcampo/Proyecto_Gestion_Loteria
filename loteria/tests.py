from datetime import date

from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse

from .models import RegistroLoteria


class SorteoCreateTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='admin', password='admin123'
        )
        self.client.force_login(
            self.user,
            backend='django.contrib.auth.backends.ModelBackend',
        )
        self.url = reverse('loteria:registrar')
        self.listado_url = reverse('loteria:listado')
        self.existing = RegistroLoteria.objects.create(
            numero=1111,
            fecha=date(2026, 7, 2),
        )

    def test_registrar_sorteo_exitoso(self):
        """ [ID: CP-001] [Tipo: Positivo]
            Descripción: Verifica que el registro válido crea un sorteo y redirige al listado | Esperado: Redirect 302 y mensaje de éxito."""
        response = self.client.post(
            self.url,
            data={
                'numero': 1234,
                'fecha': '2026-07-01',
            },
            follow=True,
        )
        self.assertRedirects(response, self.listado_url)
        self.assertTrue(RegistroLoteria.objects.filter(numero=1234).exists())
        messages = [str(message) for message in get_messages(response.wsgi_request)]
        self.assertIn('Número ganador registrado exitosamente.', messages)

    def test_registrar_sorteo_numero_invalido(self):
        """ [ID: CP-002] [Tipo: Negativo]
            Descripción: Verifica la validación de número inválido en el formulario | Esperado: HTTP 200 y error en el campo numero."""
        response = self.client.post(
            self.url,
            data={
                'numero': 0,
                'fecha': '2026-07-10',
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'loteria/registro.html')
        form = response.context['form']
        self.assertIn('numero', form.errors)
        self.assertIn('Ingrese un número ganador válido mayor que cero.', form.errors['numero'])

    def test_registrar_sorteo_fecha_duplicada(self):
        """ [ID: CP-003] [Tipo: Negativo]
            Descripción: Verifica que no se pueda registrar un sorteo con fecha duplicada | Esperado: HTTP 200 y error en el campo fecha."""
        response = self.client.post(
            self.url,
            data={
                'numero': 2222,
                'fecha': self.existing.fecha.isoformat(),
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'loteria/registro.html')
        form = response.context['form']
        self.assertIn('fecha', form.errors)
        self.assertIn(
            'Ya existe un número ganador registrado para la fecha seleccionada.',
            form.errors['fecha'],
        )

    def test_modelo_unicidad_fecha_orm(self):
        """ [ID: CP-004] [Tipo: Borde]
            Descripción: Verifica que el ORM impida dos registros con la misma fecha | Esperado: IntegrityError."""
        with self.assertRaises(IntegrityError):
            RegistroLoteria.objects.create(
                numero=2222,
                fecha=self.existing.fecha,
            )


class SorteoListTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='admin', password='admin123'
        )
        self.client.force_login(
            self.user,
            backend='django.contrib.auth.backends.ModelBackend',
        )
        self.url = reverse('loteria:consultar_sorteos')
        self.registro_antiguo = RegistroLoteria.objects.create(
            numero=100,
            fecha=date(2026, 1, 1),
        )
        self.registro_intermedio = RegistroLoteria.objects.create(
            numero=200,
            fecha=date(2026, 2, 1),
        )
        self.registro_reciente = RegistroLoteria.objects.create(
            numero=300,
            fecha=date(2026, 3, 1),
        )

    def test_listado_publico_ordena_descendentemente(self):
        """ [ID: CP-005] [Tipo: Positivo]
            Descripción: Verifica el orden cronológico descendente en la lista pública | Esperado: registros ordenados de más reciente a más antiguo."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'loteria/listado_publico.html')
        sorteos = list(response.context['sorteos'])
        self.assertEqual([s.fecha for s in sorteos], [
            self.registro_reciente.fecha,
            self.registro_intermedio.fecha,
            self.registro_antiguo.fecha,
        ])

    def test_listado_publico_filtra_por_fecha(self):
        """ [ID: CP-006] [Tipo: Positivo]
            Descripción: Verifica el filtrado por fecha vía GET | Esperado: solo el sorteo de la fecha solicitada."""
        response = self.client.get(self.url, {'fecha': self.registro_intermedio.fecha.isoformat()})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['sorteos']), 1)
        self.assertEqual(response.context['sorteos'][0].numero, self.registro_intermedio.numero)

    def test_listado_publico_vacio(self):
        """ [ID: CP-007] [Tipo: Borde]
            Descripción: Verifica el comportamiento cuando no hay sorteos registrados | Esperado: lista vacía y total_sorteos igual a cero."""
        RegistroLoteria.objects.all().delete()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['page_obj'].object_list), [])
        self.assertEqual(response.context['total_sorteos'], 0)


class SorteoUpdateTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='admin', password='admin123'
        )
        self.client.force_login(
            self.user,
            backend='django.contrib.auth.backends.ModelBackend',
        )
        self.sorteo = RegistroLoteria.objects.create(
            numero=400,
            fecha=date(2026, 4, 1),
        )
        self.otro_sorteo = RegistroLoteria.objects.create(
            numero=500,
            fecha=date(2026, 5, 1),
        )
        self.url = reverse('loteria:editar_sorteo', args=[self.sorteo.pk])
        self.listado_url = reverse('loteria:listado')

    def test_carga_formulario_edicion_get(self):
        """ [ID: CP-008] [Tipo: Positivo]
            Descripción: Verifica que la vista de edición carga el formulario con datos existentes | Esperado: HTTP 200 y formulario con instancia correcta."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'loteria/editar_sorteo.html')
        self.assertEqual(response.context['form'].instance.pk, self.sorteo.pk)
        self.assertEqual(response.context['form'].initial['numero'], self.sorteo.numero)

    def test_actualizacion_sorteo_exitosa(self):
        """ [ID: CP-009] [Tipo: Positivo]
            Descripción: Verifica la actualización exitosa de un sorteo existente | Esperado: redirect 302, mensaje de éxito y valores actualizados."""
        response = self.client.post(
            self.url,
            data={
                'numero': 401,
                'fecha': '2026-04-02',
            },
            follow=True,
        )
        self.assertRedirects(response, self.listado_url)
        self.sorteo.refresh_from_db()
        self.assertEqual(self.sorteo.numero, 401)
        self.assertEqual(self.sorteo.fecha, date(2026, 4, 2))
        messages = [str(message) for message in get_messages(response.wsgi_request)]
        self.assertIn('Sorteo actualizado correctamente.', messages)

    def test_editar_sorteo_no_existente_404(self):
        """ [ID: CP-010] [Tipo: Negativo]
            Descripción: Verifica que la edición de un sorteo inexistente devuelve 404 | Esperado: HTTP 404."""
        url = reverse('loteria:editar_sorteo', args=[9999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_conflicto_fecha_duplicada_al_actualizar(self):
        """ [ID: CP-011] [Tipo: Negativo]
            Descripción: Verifica que la edición no permite duplicar una fecha existente | Esperado: HTTP 200 y error en el campo fecha."""
        response = self.client.post(
            self.url,
            data={
                'numero': 400,
                'fecha': self.otro_sorteo.fecha.isoformat(),
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'loteria/editar_sorteo.html')
        form = response.context['form']
        self.assertIn('fecha', form.errors)
        self.assertIn(
            'Ya existe un número ganador registrado para la fecha seleccionada.',
            form.errors['fecha'],
        )


class SorteoDeleteTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='admin', password='admin123'
        )
        self.client.force_login(
            self.user,
            backend='django.contrib.auth.backends.ModelBackend',
        )
        self.sorteo = RegistroLoteria.objects.create(
            numero=600,
            fecha=date(2026, 6, 1),
        )
        self.url = reverse('loteria:eliminar_sorteo', args=[self.sorteo.pk])
        self.listado_url = reverse('loteria:listado')

    def test_borrar_sorteo_via_post(self):
        """ [ID: CP-012] [Tipo: Positivo]
            Descripción: Verifica que el borrado por POST elimina el registro y redirige al listado | Esperado: registro eliminado y mensaje de confirmación."""
        response = self.client.post(self.url, follow=True)
        self.assertRedirects(response, self.listado_url)
        self.assertFalse(RegistroLoteria.objects.filter(pk=self.sorteo.pk).exists())
        messages = [str(message) for message in get_messages(response.wsgi_request)]
        self.assertTrue(any('eliminado permanentemente' in message for message in messages))

    def test_borrar_sorteo_no_existente_404(self):
        """ [ID: CP-013] [Tipo: Negativo]
            Descripción: Verifica que intentar borrar un sorteo inexistente devuelve 404 | Esperado: HTTP 404."""
        url = reverse('loteria:eliminar_sorteo', args=[9999])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 404)
