def generate_latex_header():
    header = """\centering
\\begin{tabular}{rlrrrrrrrrr}
Pixels & Mode & $p$-beam & $p_{\\text{use}}$ & $\Fevent$ & $\Trun$ & $\Treduction$ & $\\Ncore$ & $\langle\\Ncore\\rangle$ & $\\Mcore$ \\\\
& & $[\mathrm{MW}]$ & & $\mathrm{[s^{-1}]}$ & $\mathrm{[s]}$ & $\mathrm{[s]}$ & & & [GByte]\\\\
\hline
"""
    return header

def generate_latex_footer():
    header = """\hline
\end{tabular}
"""
    return header

class LatexTabular:
    def __init__(self, config_count, speedup):
        self.lines = []
        self.config_count = config_count
        self.speedup = speedup
        self.power_count = 5

    def set_pixel_count(self, pixels):
        self.lines.append('\hline\n')
        self.lines.append('\multirow{{{}}}{{*}}{{{}}}\n'.format(self.config_count * self.power_count, pixels)) 

    def set_config(self, name):
        self.lines.append('\\\[-2.0ex]& \multirow{{{}}}{{*}}{{{}}}\n'.format(self.power_count, name))
        self.power = 0

    def add(self, power, use_fraction, event_rate, t_run, t_reduction, *args):
        columns = len(args)+7
        float_str = "{0:.2g}".format(event_rate)
        event_rate_base, exponent = float_str.split("e")
        event_rate_exponent = int(exponent)
        if t_reduction > 30 and t_run < self.speedup*t_reduction:
            base = ('& {:4.1f} & {} & ${}\cdot 10^{:1}$ & {:8.1f} & \\textcolor{{red}}{{{:6.0f}}} & {:4} & {:6.0f} & {:4.0f}' + '\\\\').format(power, use_fraction, event_rate_base, event_rate_exponent, t_run, t_reduction, *args)
        else:
            base = ('& {:4.1f} & {} & ${}\cdot 10^{:1}$ & {:8.1f} & {:6.0f} & {:4} & {:6.0f} & {:4.0f}' + '\\\\').format(power, use_fraction, event_rate_base, event_rate_exponent, t_run, t_reduction, *args)
        if self.power == 0:
            self.lines.append(base + '\n')
        elif self.power == 4:
            self.lines.append('&' + base + '\cline{{2-{}}}\n'.format(columns))
        else:
            self.lines.append('&' + base + '\n')
        self.power += 1
