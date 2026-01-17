Wakefield definitions
---------------------

Transverse wakefields are defined such that the transverse kicks are given by:

.. math::

    \Delta p_x &=
     \frac{q^2 e^2}{m_0 \gamma \beta_0^2 c^2}
     \sum_{i,j,k,l \ge 0}
        x^k y^l \int_{-\infty}^{\infty}
        \bar{x}^i(z')\,\bar{y}^j(z')\,\lambda(z')\,W^{i,j,k,l}_{x}(z - z')\,dz' \\
    \Delta p_y &=
     \frac{q^2 e^2}{m_0 \gamma \beta_0^2 c^2}
     \sum_{i,j,k,l \ge 0}
        x^k y^l \int_{-\infty}^{\infty}
        \bar{x}^i(z')\,\bar{y}^j(z')\,\lambda(z')\,W^{i,j,k,l}_{y}(z - z')\,dz'

where :math:`\bar{x}(z)` and :math:`\bar{y}(z)` are the transverse centroids,
and :math:`\lambda(z)` is the line density. The exponents :math:`(i,j)` belong
to the source moments, while :math:`(k,l)` apply to the test particle offsets.

Longitudinal kicks are defined so that the energy momentum deviation change is:

.. math::

    \Delta \delta = -\frac{q^2 e^2}{m_0 \gamma \beta_0^2 c^2}
    \int_{-\infty}^{\infty} \lambda(z')\, W_s(z - z')\,dz' ~,

with the sign convention that a positive wake causes energy loss.

Each predefined ``kind`` maps to a plane and to a set of source exponents
:math:`(i,j)` and test exponents :math:`(k,l)`, following :math:`W^{i,j,k,l}` in 
the formulas above. The available kinds are listed below:

.. list-table::
   :widths: 20 8 18 18 36
   :header-rows: 1

   * - kind
     - plane
     - source_exponents
     - test_exponents
     - meaning
   * - ``longitudinal``
     - z
     - (0, 0)
     - (0, 0)
     - longitudinal
   * - ``constant_x``
     - x
     - (0, 0)
     - (0, 0)
     - constant x
   * - ``constant_y``
     - y
     - (0, 0)
     - (0, 0)
     - constant y
   * - ``dipolar_x``
     - x
     - (1, 0)
     - (0, 0)
     - dipolar / driving x
   * - ``dipolar_y``
     - y
     - (0, 1)
     - (0, 0)
     - dipolar / driving y
   * - ``dipolar_xy``
     - x
     - (0, 1)
     - (0, 0)
     - dipolar / driving xy
   * - ``dipolar_yx``
     - y
     - (1, 0)
     - (0, 0)
     - dipolar / driving yx
   * - ``quadrupolar_x``
     - x
     - (0, 0)
     - (1, 0)
     - quadrupolar / detuning x
   * - ``quadrupolar_y``
     - y
     - (0, 0)
     - (0, 1)
     - quadrupolar / detuning y
   * - ``quadrupolar_xy``
     - x
     - (0, 0)
     - (0, 1)
     - quadrupolar / detuning xy
   * - ``quadrupolar_yx``
     - y
     - (0, 0)
     - (1, 0)
     - quadrupolar / detuning yx

Wakefield objects can be initialized in different ways, as illustrated by the following
examples.


Single component
    .. code-block:: python

        # Horizontal dipolar resonator
        w1 = xw.WakeResonator(kind='dipolar_x', r=1e8, q=1e5, f_r=1e9)

Multiple components (list/tuple)
    .. code-block:: python

        # Horizontal + vertical dipolar with same r/q/f_r
        w2 = xw.WakeResonator(kind=['dipolar_x', 'dipolar_y'],
                              r=1e8, q=1e5, f_r=1e9)

Weighted components (dict)
    .. code-block:: python

        # Scale horizontal twice as strong as vertical
        w3 = xw.WakeResonator(kind={'dipolar_x': 2.0, 'dipolar_y': 1.0},
                              r=1e8, q=1e5, f_r=1e9)

Using Yokoya factors
    .. code-block:: python

        # Flat chamber (horizontal) yokoya factors expanded into the right components
        w4 = xw.WakeResonator(kind=xw.Yokoya('flat_horizontal'),
                              r=1e8, q=1e5, f_r=1e9)

Custom polynomial term
    .. code-block:: python

        # Custom plane/exponents without a predefined kind entry
        w5 = xw.WakeResonator(
            plane='y',
            source_exponents=(1, 0),  # x_source^1 y_source^0
            test_exponents=(0, 2),    # x_test^0 y_test^2
            r=1e8, q=1e5, f_r=1e9)

Combine and configure
    .. code-block:: python

        w = w1 + w2 + w3.components[0]  # mix whole wakes and single components
        w.configure_for_tracking(zeta_range=(-0.1, 0.1), num_slices=200)