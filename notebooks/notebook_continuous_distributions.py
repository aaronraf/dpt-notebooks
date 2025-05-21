# Title: Continuous Distributions
# Description: Visualization of Probability Density Functions (PDFs) and Cumulative Distribution Functions (CDFs) for several common continuous distributions
# Tags: chap-1, pdf, cdf
# Date: 2025-05-07

import marimo

__generated_with = "0.13.2"
app = marimo.App()


@app.cell(hide_code=True)
def _():
    # %% Imports and Setup
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt
    from scipy import stats
    import math

    # Constants
    NUM_POINTS = 400  # Number of points for smooth curves
    EPS = 1e-9        # Small epsilon for numerical stability near boundaries

    mo.md(
        """
        # Visualizing Common Continuous Probability Distributions

        This notebook interactively visualizes the Probability Density Functions (PDFs)
        and Cumulative Distribution Functions (CDFs) for several common continuous
        distributions defined on $\mathbb{R}$ or subsets thereof.
        """
    )
    return EPS, NUM_POINTS, mo, np, plt, stats


@app.cell(hide_code=True)
def _(plt):
    # %% Helper function for Plotting Continuous Distributions (with fixed axes support)
    def plot_pdf_cdf(x, pdf, cdf, title_prefix, x_min_plot, x_max_plot, y_max_pdf):
        """Generates PDF and CDF plots for a continuous distribution using specified axes."""
        fig, (ax_pdf, ax_cdf) = plt.subplots(1, 2, figsize=(12, 5))

        # --- PDF Plot ---
        ax_pdf.plot(x, pdf, 'C0-', lw=2)
        ax_pdf.set_xlabel("x")
        ax_pdf.set_ylabel("f(x)") # Density
        ax_pdf.set_title("Probability Density Function (PDF)")
        ax_pdf.grid(True, linestyle=':')
        ax_pdf.set_xlim(x_min_plot, x_max_plot) # Use fixed limits
        ax_pdf.set_ylim(bottom=0, top=y_max_pdf) # Use fixed limits
        ax_pdf.axhline(0, color='black', linewidth=0.5) # Emphasize y=0 axis


        # --- CDF Plot ---
        ax_cdf.plot(x, cdf, 'C1-', lw=2)
        ax_cdf.set_xlabel("x")
        ax_cdf.set_ylabel("F(x) = P(X ≤ x)")
        ax_cdf.set_title("Cumulative Distribution Function (CDF)")
        ax_cdf.grid(True, linestyle=':')
        ax_cdf.set_xlim(x_min_plot, x_max_plot) # Match PDF x-range
        ax_cdf.set_ylim(-0.05, 1.05) # CDF y-range is naturally fixed
        ax_cdf.axhline(0, color='black', linewidth=0.5)
        ax_cdf.axhline(1, color='black', linewidth=0.5, linestyle='--')


        fig.suptitle(title_prefix, fontsize=14)
        plt.tight_layout(rect=[0, 0.03, 1, 0.93]) # Adjust layout
        plt.close(fig) # Close the figure to prevent double display, Marimo gets the object
        return fig

    return (plot_pdf_cdf,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## 1. Uniform Distribution
        For $a,b\in\mathbb{R}$ with $a<b$, the $\mathrm{Unif}(a,b)$ distribution has support $\Omega=[a,b]$ and PDF:
        $$p_{\mathrm{Unif}(a,b)}(x) =
        \begin{cases}
            \dfrac{1}{b-a}, & a \le x \le b,\\[0.5em]
            0, & \text{otherwise}.
        \end{cases}$$
        *(Note: Fixed axes are used, which might clip the view if $a$ or $b$ are outside [-10, 10].)*
        """
    )
    return


@app.cell
def _(mo):
    # %% Uniform Sliders Definition
    uniform_a = mo.ui.slider(-10.0, 10.0, value=2.0, step=0.1, label="Lower bound (a):")
    uniform_b = mo.ui.slider(-10.0, 10.0, value=5.0, step=0.1, label="Upper bound (b):")

    # Just display the sliders here
    ui_sliders = mo.vstack([uniform_a, uniform_b])
    ui_sliders
    return uniform_a, uniform_b


@app.cell
def _(mo, uniform_a, uniform_b):
    # %% Uniform Warning Display (Reads values from sliders defined above)
    warning_message = mo.md(r"$\qquad \color{red} \text{Warning: } a \text{ must be less than } b$")

    # Display warning only if needed
    warning_display = warning_message if uniform_a.value >= uniform_b.value - 1e-6 else None
    warning_display
    return


@app.cell(hide_code=True)
def _(EPS, NUM_POINTS, np, plot_pdf_cdf, stats, uniform_a, uniform_b):
    # %% Uniform Calculation
    _a_u = uniform_a.value # Read value here (allowed, depends on slider cell)
    _b_u = uniform_b.value # Read value here

    # --- Define Fixed Axes for Uniform Plot ---
    _X_MIN_FIXED_U = -10.5
    _X_MAX_FIXED_U = 10.5
    _Y_MAX_PDF_FIXED_U = 1.5

    # Calculate over a slightly wider range than the plot window
    x_unif_calc = np.linspace(_X_MIN_FIXED_U - 1, _X_MAX_FIXED_U + 1, NUM_POINTS*2)
    pdf_unif = np.zeros_like(x_unif_calc)
    cdf_unif = np.zeros_like(x_unif_calc)

    if _a_u < _b_u:
        dist_unif = stats.uniform(loc=_a_u, scale=_b_u - _a_u)
        pdf_unif = dist_unif.pdf(x_unif_calc)
        cdf_unif = dist_unif.cdf(x_unif_calc)
        cdf_unif[x_unif_calc > _b_u] = 1.0
    else:
        pass # pdf/cdf remain zeros

    # Use integer display if parameters are effectively integers
    _a_u_str = int(_a_u) if abs(_a_u - round(_a_u)) < EPS else f"{_a_u:.1f}"
    _b_u_str = int(_b_u) if abs(_b_u - round(_b_u)) < EPS else f"{_b_u:.1f}"
    _title_u = f"Uniform Distribution (a={_a_u_str}, b={_b_u_str})"
    if _a_u >= _b_u:
        _title_u += " (Invalid: a ≥ b)"

    # %% Uniform Plot
    fig_uniform = plot_pdf_cdf(
        x_unif_calc, pdf_unif, cdf_unif,
        _title_u,
        x_min_plot = _X_MIN_FIXED_U,
        x_max_plot = _X_MAX_FIXED_U,
        y_max_pdf = _Y_MAX_PDF_FIXED_U
    )
    fig_uniform    # No return needed if fig_uniform is the last expression
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## 2. Normal Distribution
        For $\mu\in\mathbb{R}$ (mean) and $\sigma>0$ (standard deviation), the $\mathcal{N}(\mu,\sigma^2)$ distribution has support $\Omega=\mathbb{R}$ and PDF:
        $$p_{\mathcal{N}(\mu,\sigma^2)}(x) = \frac{1}{\sqrt{2\pi}\,\sigma} \exp\!\Bigl(-\tfrac{(x-\mu)^2}{2\sigma^2}\Bigr).$$
        *(Note: $\sigma^2$ is the variance)*
        """
    )
    return


@app.cell
def _(mo):
    # %% Normal Sliders
    norm_mu = mo.ui.slider(-10.0, 10.0, value=0.0, step=0.1, label="Mean (μ):")
    norm_sigma = mo.ui.slider(0.1, 5.0, value=1.5, step=0.1, label="Standard Deviation (σ):") # Reduced max sigma for visibility

    mo.vstack([norm_mu, norm_sigma]) # Display UI
    return norm_mu, norm_sigma


@app.cell(hide_code=True)
def _(EPS, NUM_POINTS, norm_mu, norm_sigma, np, plot_pdf_cdf, stats):
    # %% Normal Calculation
    _mu_n = norm_mu.value
    _sigma_n = norm_sigma.value
    _var_n = _sigma_n**2

    # --- Define Fixed Axes for Normal Plot ---
    _X_MIN_FIXED_N = -15.0
    _X_MAX_FIXED_N = 15.0
    _Y_MAX_PDF_FIXED_N = 1.0 # Reduced from 4 (max for sigma=0.1) for better view of typical sigmas

    # Calculate over a wider range than the plot window for smooth edges
    x_norm_calc = np.linspace(_X_MIN_FIXED_N - 5, _X_MAX_FIXED_N + 5, NUM_POINTS*2)
    pdf_norm = np.zeros_like(x_norm_calc)
    cdf_norm = np.zeros_like(x_norm_calc)

    if _sigma_n > 0:
        dist_norm = stats.norm(loc=_mu_n, scale=_sigma_n)
        pdf_norm = dist_norm.pdf(x_norm_calc)
        cdf_norm = dist_norm.cdf(x_norm_calc)

    # Format parameters for title
    _mu_n_str = int(_mu_n) if abs(_mu_n - round(_mu_n)) < EPS else f"{_mu_n:.1f}"
    _var_n_str = int(_var_n) if abs(_var_n - round(_var_n)) < EPS else f"{_var_n:.2f}"
    _title_n = f"Normal Distribution (μ={_mu_n_str}, σ²={_var_n_str})"

    # %% Normal Plot
    fig_norm = plot_pdf_cdf(
        x_norm_calc, pdf_norm, cdf_norm,
        _title_n,
        x_min_plot=_X_MIN_FIXED_N, # Use fixed axes
        x_max_plot=_X_MAX_FIXED_N,
        y_max_pdf=_Y_MAX_PDF_FIXED_N
    )
    fig_norm
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## 3. Gamma Distribution
        For shape $\alpha>0$ and rate $\beta>0$, the $\Gamma(\alpha,\beta)$ distribution has support $\Omega=(0,\infty)$ and PDF:
        $$p_{\Gamma(\alpha,\beta)}(x) = \frac{\beta^\alpha}{\Gamma(\alpha)}\,x^{\alpha-1}e^{-\beta x}.$$
        *(Note: `scipy.stats.gamma` uses shape $a=\alpha$ and **scale** $\theta = 1/\beta$)*.
        """
    )
    return


@app.cell
def _(mo):
    # %% Gamma Sliders
    gamma_alpha = mo.ui.slider(0.5, 10.0, value=3.0, step=0.1, label="Shape (α):") # alpha > 0, start at 0.5 for visibility
    gamma_beta = mo.ui.slider(0.1, 5.0, value=0.5, step=0.1, label="Rate (β):")   # beta > 0, reduced max beta

    mo.vstack([gamma_alpha, gamma_beta]) # Display UI
    return gamma_alpha, gamma_beta


@app.cell(hide_code=True)
def _(EPS, NUM_POINTS, gamma_alpha, gamma_beta, np, plot_pdf_cdf, stats):
    # %% Gamma Calculation
    _alpha_g = gamma_alpha.value
    _beta_g = gamma_beta.value

    # --- Define Fixed Axes for Gamma Plot ---
    _X_MIN_FIXED_G = -1.0 # Start slightly below 0 for visual frame
    _X_MAX_FIXED_G = 50.0
    _Y_MAX_PDF_FIXED_G = 1.0 # Adjusted for typical shapes in slider range

    # Calculate over relevant range (0 to slightly beyond x_max)
    x_gamma_calc = np.linspace(EPS, _X_MAX_FIXED_G + 5, NUM_POINTS*2) # Start calculation just above 0
    # Need to prepend a point at x=0 (or EPS) for plotting continuity if needed
    x_gamma_calc = np.insert(x_gamma_calc, 0, EPS)
    pdf_gamma = np.zeros_like(x_gamma_calc)
    cdf_gamma = np.zeros_like(x_gamma_calc)


    if _alpha_g > 0 and _beta_g > 0:
        _scale_g = 1.0 / _beta_g
        dist_gamma = stats.gamma(a=_alpha_g, scale=_scale_g)
        pdf_gamma = dist_gamma.pdf(x_gamma_calc)
        cdf_gamma = dist_gamma.cdf(x_gamma_calc)
        pdf_gamma = np.nan_to_num(pdf_gamma) # Handle potential issues near 0 if alpha < 1
        cdf_gamma = np.nan_to_num(cdf_gamma)
        # Ensure pdf is 0 for x<=0 visually
        pdf_gamma[x_gamma_calc <= EPS] = 0
        cdf_gamma[x_gamma_calc <= EPS] = 0


    # Format parameters for title
    _alpha_g_str = int(_alpha_g) if abs(_alpha_g - round(_alpha_g)) < EPS else f"{_alpha_g:.1f}"
    _beta_g_str = int(_beta_g) if abs(_beta_g - round(_beta_g)) < EPS else f"{_beta_g:.1f}"
    _title_g = f"Gamma Distribution (α={_alpha_g_str}, β={_beta_g_str})"

    # %% Gamma Plot
    fig_gamma = plot_pdf_cdf(
        x_gamma_calc, pdf_gamma, cdf_gamma,
        _title_g,
        x_min_plot=_X_MIN_FIXED_G, # Use fixed axes
        x_max_plot=_X_MAX_FIXED_G,
        y_max_pdf=_Y_MAX_PDF_FIXED_G
    )
    fig_gamma
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 3a. Exponential Distribution (Special case of Gamma)
        The $\mathrm{Exp}(\lambda)$ distribution with rate $\lambda>0$ is $\Gamma(1,\lambda)$. Support $\Omega=(0,\infty)$ and PDF:
        $$p_{\mathrm{Exp}(\lambda)}(x) = \lambda e^{-\lambda x},\quad x>0.$$
        *(Note: `scipy.stats.expon` uses **scale** = $1/\lambda$)*.
        """
    )
    return


@app.cell
def _(mo):
    # %% Exponential Slider
    exp_lambda = mo.ui.slider(0.1, 5.0, value=1.5, step=0.1, label="Rate (λ):") # lambda > 0, reduced max lambda
    exp_lambda # Display UI
    return (exp_lambda,)


@app.cell(hide_code=True)
def _(EPS, NUM_POINTS, exp_lambda, np, plot_pdf_cdf, stats):
    # %% Exponential Calculation
    _lambda_e = exp_lambda.value

    # --- Define Fixed Axes for Exponential Plot ---
    _X_MIN_FIXED_E = -1.0 # Start slightly below 0 for visual frame
    _X_MAX_FIXED_E = 15.0
    _Y_MAX_PDF_FIXED_E = 5.0 # Max value is lambda

    # Calculate over relevant range (0 to slightly beyond x_max)
    x_exp_calc = np.linspace(EPS, _X_MAX_FIXED_E + 2, NUM_POINTS*2) # Start calc just above 0
    x_exp_calc = np.insert(x_exp_calc, 0, EPS)
    pdf_exp = np.zeros_like(x_exp_calc)
    cdf_exp = np.zeros_like(x_exp_calc)

    if _lambda_e > 0:
        _scale_e = 1.0 / _lambda_e
        dist_exp = stats.expon(scale=_scale_e)
        pdf_exp = dist_exp.pdf(x_exp_calc)
        cdf_exp = dist_exp.cdf(x_exp_calc)
        # Ensure pdf/cdf are 0 for x<=0 visually
        pdf_exp[x_exp_calc <= EPS] = 0
        cdf_exp[x_exp_calc <= EPS] = 0

    # Format parameters for title
    _lambda_e_str = int(_lambda_e) if abs(_lambda_e - round(_lambda_e)) < EPS else f"{_lambda_e:.1f}"
    _title_e = f"Exponential Distribution (λ={_lambda_e_str})"

    # %% Exponential Plot
    fig_exp = plot_pdf_cdf(
        x_exp_calc, pdf_exp, cdf_exp,
        _title_e,
        x_min_plot=_X_MIN_FIXED_E, # Use fixed axes
        x_max_plot=_X_MAX_FIXED_E,
        y_max_pdf=_Y_MAX_PDF_FIXED_E
    )
    fig_exp
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 3b. Chi-squared Distribution (Special case of Gamma)
        The $\chi^2_k$ distribution with $k>0$ degrees of freedom is $\Gamma(k/2, 1/2)$. Support $\Omega=(0,\infty)$ and PDF:
        $$p_{\chi^2_k}(x) = \frac{1}{2^{k/2}\Gamma(k/2)}\,x^{k/2-1}e^{-x/2},\quad x>0.$$
        *(Note: `scipy.stats.chi2` uses degrees of freedom `df` = $k$)*.
        """
    )
    return


@app.cell
def _(mo):
    # %% Chi-squared Slider
    chi2_k = mo.ui.slider(1, 30, value=4, step=1, label="Degrees of Freedom (k):") # k is integer > 0, reduced max k
    chi2_k # Display UI
    return (chi2_k,)


@app.cell(hide_code=True)
def _(EPS, NUM_POINTS, chi2_k, np, plot_pdf_cdf, stats):
    # %% Chi-squared Calculation
    _k_c = chi2_k.value

    # --- Define Fixed Axes for Chi-squared Plot ---
    _X_MIN_FIXED_C = -2.0 # Start slightly below 0 for visual frame
    _X_MAX_FIXED_C = 40.0
    _Y_MAX_PDF_FIXED_C = 0.5 # Adjusted for typical shapes

    # Calculate over relevant range (0 to slightly beyond x_max)
    x_chi2_calc = np.linspace(EPS, _X_MAX_FIXED_C + 5, NUM_POINTS*2) # Start calc just above 0
    x_chi2_calc = np.insert(x_chi2_calc, 0, EPS)
    pdf_chi2 = np.zeros_like(x_chi2_calc)
    cdf_chi2 = np.zeros_like(x_chi2_calc)


    if _k_c >= 1:
        dist_chi2 = stats.chi2(df=_k_c)
        pdf_chi2 = dist_chi2.pdf(x_chi2_calc)
        cdf_chi2 = dist_chi2.cdf(x_chi2_calc)
        pdf_chi2 = np.nan_to_num(pdf_chi2) # Handle potential inf at x=0 for k=1, 2
        # Ensure pdf/cdf are 0 for x<=0 visually
        pdf_chi2[x_chi2_calc <= EPS] = 0
        cdf_chi2[x_chi2_calc <= EPS] = 0

    # Format parameters for title
    _title_c = f"Chi-squared Distribution (k={_k_c})" # k is integer

    # %% Chi-squared Plot
    fig_chi2 = plot_pdf_cdf(
        x_chi2_calc, pdf_chi2, cdf_chi2,
        _title_c,
        x_min_plot=_X_MIN_FIXED_C, # Use fixed axes
        x_max_plot=_X_MAX_FIXED_C,
        y_max_pdf=_Y_MAX_PDF_FIXED_C
    )
    fig_chi2
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## 4. Student's t Distribution
        For $\nu>0$ degrees of freedom, the $t_\nu$ distribution has support $\Omega=\mathbb{R}$ and PDF:
        $$p_{t_\nu}(x) = \frac{\Gamma\!\bigl(\tfrac{\nu+1}{2}\bigr)}{\sqrt{\nu\pi}\,\Gamma\!\bigl(\tfrac{\nu}{2}\bigr)} \Bigl(1 + \tfrac{x^2}{\nu}\Bigr)^{-\tfrac{\nu+1}{2}}.$$
        *(Note: `scipy.stats.t` uses degrees of freedom `df` = $\nu$)*.
        """
    )
    return


@app.cell
def _(mo):
    # %% Student's t Slider
    t_nu = mo.ui.slider(1, 30, value=5, step=1, label="Degrees of Freedom (ν):") # nu is integer > 0, reduced max nu
    t_nu # Display UI
    return (t_nu,)


@app.cell(hide_code=True)
def _(NUM_POINTS, np, plot_pdf_cdf, stats, t_nu):
    # %% Student's t Calculation
    _nu_t = t_nu.value

    # --- Define Fixed Axes for Student's t Plot ---
    _X_MIN_FIXED_T = -8.0
    _X_MAX_FIXED_T = 8.0
    _Y_MAX_PDF_FIXED_T = 0.45 # Max density is ~0.4 for large nu (like Normal)

    # Calculate over a wider range than the plot window for smooth edges
    x_t_calc = np.linspace(_X_MIN_FIXED_T - 2, _X_MAX_FIXED_T + 2, NUM_POINTS*2)
    pdf_t = np.zeros_like(x_t_calc)
    cdf_t = np.zeros_like(x_t_calc)

    if _nu_t >= 1:
        dist_t = stats.t(df=_nu_t)
        pdf_t = dist_t.pdf(x_t_calc)
        cdf_t = dist_t.cdf(x_t_calc)

    # Format parameters for title
    _title_t = f"Student's t Distribution (ν={_nu_t})" # nu is integer

    # %% Student's t Plot
    fig_t = plot_pdf_cdf(
        x_t_calc, pdf_t, cdf_t,
        _title_t,
        x_min_plot = _X_MIN_FIXED_T, # Use fixed axes
        x_max_plot = _X_MAX_FIXED_T,
        y_max_pdf = _Y_MAX_PDF_FIXED_T
    )
    fig_t
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## 5. Beta Distribution
        For $\alpha>0$, $\beta>0$, the $\mathrm{Beta}(\alpha,\beta)$ distribution has support $\Omega=[0,1]$ (or $(0,1)$ if $\alpha<1$ or $\beta<1$) and PDF:
        $$p_{\mathrm{Beta}(\alpha,\beta)}(x) = \frac{x^{\alpha-1}(1-x)^{\beta-1}}{B(\alpha,\beta)},\quad 0\le x\le1.$$
        where $B(\alpha,\beta) = \frac{\Gamma(\alpha)\Gamma(\beta)}{\Gamma(\alpha+\beta)}$ is the Beta function.
        *(Note: `scipy.stats.beta` uses parameters $a=\alpha$ and $b=\beta$)*.
        """
    )
    return


@app.cell
def _(mo):
    # %% Beta Sliders
    beta_alpha = mo.ui.slider(0.5, 10.0, value=2.0, step=0.1, label="Shape (α):") # alpha > 0, start 0.5
    beta_beta = mo.ui.slider(0.5, 10.0, value=5.0, step=0.1, label="Shape (β):")   # beta > 0, start 0.5

    mo.vstack([beta_alpha, beta_beta]) # Display UI
    return beta_alpha, beta_beta


@app.cell(hide_code=True)
def _(EPS, NUM_POINTS, beta_alpha, beta_beta, np, plot_pdf_cdf, stats):
    # %% Beta Calculation
    _alpha_b = beta_alpha.value
    _beta_b = beta_beta.value

    # --- Define Fixed Axes for Beta Plot ---
    # Support is [0, 1], plot slightly wider for visuals
    _X_MIN_FIXED_B = -0.1
    _X_MAX_FIXED_B = 1.1
    _Y_MAX_PDF_FIXED_B = 5.0 # Allow for high peaks when alpha/beta < 1

    # Calculate strictly within (0, 1) to avoid potential division by zero at ends,
    # then extend plotting range. Use more points for potentially sharp peaks.
    x_beta_calc = np.linspace(EPS, 1.0 - EPS, NUM_POINTS * 2)
    # Create arrays to hold results including endpoints for plotting
    x_beta_plot = np.concatenate(([0.0], x_beta_calc, [1.0]))
    pdf_beta_plot = np.zeros_like(x_beta_plot)
    cdf_beta_plot = np.zeros_like(x_beta_plot)


    if _alpha_b > 0 and _beta_b > 0:
        dist_beta = stats.beta(a=_alpha_b, b=_beta_b)
        # Calculate PDF/CDF on the inner points
        pdf_beta_inner = dist_beta.pdf(x_beta_calc)
        cdf_beta_inner = dist_beta.cdf(x_beta_calc)
        pdf_beta_inner = np.nan_to_num(pdf_beta_inner) # Handle potential inf
        cdf_beta_inner = np.nan_to_num(cdf_beta_inner)

        # Populate the plot arrays
        pdf_beta_plot[1:-1] = pdf_beta_inner
        cdf_beta_plot[1:-1] = cdf_beta_inner
        # Handle endpoints for CDF
        cdf_beta_plot[0] = 0.0
        cdf_beta_plot[-1] = 1.0
        # Handle endpoints for PDF (can be tricky if infinite)
        # If pdf goes to infinity, nan_to_num might make it large, leave as is.
        # If pdf goes to 0 or finite value, calculate it.
        try:
            pdf_at_0 = dist_beta.pdf(0)
            pdf_beta_plot[0] = np.nan_to_num(pdf_at_0) if np.isfinite(pdf_at_0) else 0 # Avoid plotting inf directly
        except ValueError: pass # pdf might not be defined at 0
        try:
            pdf_at_1 = dist_beta.pdf(1)
            pdf_beta_plot[-1] = np.nan_to_num(pdf_at_1) if np.isfinite(pdf_at_1) else 0 # Avoid plotting inf directly
        except ValueError: pass # pdf might not be defined at 1



    # Format parameters for title
    _alpha_b_str = int(_alpha_b) if abs(_alpha_b - round(_alpha_b)) < EPS else f"{_alpha_b:.1f}"
    _beta_b_str = int(_beta_b) if abs(_beta_b - round(_beta_b)) < EPS else f"{_beta_b:.1f}"
    _title_b = f"Beta Distribution (α={_alpha_b_str}, β={_beta_b_str})"

    # %% Beta Plot
    fig_beta = plot_pdf_cdf(
        x_beta_plot, pdf_beta_plot, cdf_beta_plot, # Use arrays with endpoints
        _title_b,
        x_min_plot=_X_MIN_FIXED_B, # Use fixed axes
        x_max_plot=_X_MAX_FIXED_B,
        y_max_pdf=_Y_MAX_PDF_FIXED_B
    )
    fig_beta
    return


if __name__ == "__main__":
    app.run()
