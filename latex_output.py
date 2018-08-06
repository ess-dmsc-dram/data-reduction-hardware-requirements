def generate_latex_header():
    header = """\centering
\\begin{tabular}{rlrrrrrrrrr}
Pixels & Mode & $p$-beam & Use & $\Fevent$ & $\Trun$ & $\Treduction$ & $\\Ncore$ & $\langle\\Ncore\\rangle$ & RAM\\\\
& & $[\mathrm{MW}]$ & [\%] & $\mathrm{[s^{-1}]}$ & $\mathrm{[s]}$ & $\mathrm{[s]}$ & & & [GByte/core]\\\\
\hline
"""
    return header

def generate_latex_footer():
    header = """\hline
\end{tabular}
"""
    return header

class LatexTabular:
    def __init__(self, config_count):
        self.lines = []
        self.config_count = config_count
        self.power_count = 5

    def set_pixel_count(self, pixels):
        self.lines.append('\hline\n')
        self.lines.append('\multirow{{{}}}{{*}}{{{}}}\n'.format(self.config_count * self.power_count, pixels)) 

    def set_config(self, name):
        self.lines.append('& \multirow{{{}}}{{*}}{{{}}}\n'.format(self.power_count, name))
        self.power = 0

    def add(self, power, use_fraction, *args):
        columns = len(args)+1
        base = ('& {:4.1f} & {:2.0f} & {:6.0} & {:8.1f} & {:6.0f} & {:4} & {:6.0f} & {:4.0f}' + '\\\\').format(power, 100*use_fraction, *args)
        if self.power == 0:
            self.lines.append(base + '\n')
        elif self.power == 4:
            self.lines.append('&' + base + '\cline{{2-{}}}\n'.format(columns+3))
        else:
            self.lines.append('&' + base + '\n')
        self.power += 1
