
def clip(v, lo, hi):
    if v < lo:
        return lo
    elif v > hi:
        return hi
    else:
        return v


def bargraph(x, mn, mx, w, c='X'):
    '''Draws a simple asciiart bar graph. Very handy for
    visualizing what's going on with the data.
    x= Value from sensor, mn= minimum plottable value,
    mx= maximum plottable value, w= width of plot in chars,
    c= the character to plot with.'''
    if not w: return ''  # No width!
    if x < mn: x = mn  # Clip to bounds.
    if x > mx: x = mx  # Clip to bounds.
    tx = mx - mn  # Total real units possible to show on graph.
    if tx <= 0: return 'backwards'  # Stupid bounds.
    upw = tx / float(w)  # X Units per output char width.
    if upw <= 0: return 'what?'  # Don't let this happen.
    negpu, pospu, negnonpu, posnonpu = 0, 0, 0, 0
    if mn < 0:  # Then there is a negative part to graph.
        if x < 0:  # And the plot is on the negative side.
            negpu = -x + min(0, mx)
            negnonpu = -mn + x
        else:  # Plot is on pos. Neg side is empty.
            negnonpu = -mn + min(0, mx)  # But still show some empty neg.
    if mx > 0:  # There is a positive part to the graph
        if x > 0:  # And the plot is on the positive side.
            pospu = x - max(0, mn)
            posnonpu = mx - x
        else:  # Plot is on neg. Pos side is empty.
            posnonpu = mx - max(0, mn)  # But still show some empty pos.
    nnc = int(negnonpu / upw) * '-'
    npc = int(negpu / upw) * c
    ppc = int(pospu / upw) * c
    pnc = int(posnonpu / upw) * '_'
    return '[%s]' % (nnc + npc + ppc + pnc)

class ServerState():
    '''What the server is reporting right now.'''

    def __init__(self):
        self.servstr = str()
        self.d = dict()

    def parse_server_str(self, server_string):
        '''Parse the server string.'''
        self.servstr = server_string.strip()[:-1]
        sslisted = self.servstr.strip().lstrip('(').rstrip(')').split(')(')
        for i in sslisted:
            w = i.split(' ')
            self.d[w[0]] = destringify(w[1:])

    def __repr__(self):
        # Comment the next line for raw output:
        return self.fancyout()
        # -------------------------------------
        out = str()
        for k in sorted(self.d):
            strout = str(self.d[k])
            if type(self.d[k]) is list:
                strlist = [str(i) for i in self.d[k]]
                strout = ', '.join(strlist)
            out += "%s: %s\n" % (k, strout)
        return out

    def fancyout(self):
        '''Specialty output for useful ServerState monitoring.'''
        out = str()
        sensors = [  # Select the ones you want in the order you want them.
            # 'curLapTime',
            # 'lastLapTime',
            'stucktimer',
            # 'damage',
            # 'focus',
            'fuel',
            # 'gear',
            'distRaced',
            'distFromStart',
            # 'racePos',
            'opponents',
            'wheelSpinVel',
            'z',
            'speedZ',
            'speedY',
            'speedX',
            'targetSpeed',
            'rpm',
            'skid',
            'slip',
            'track',
            'trackPos',
            'angle',
        ]

        # for k in sorted(self.d): # Use this to get all sensors.
        for k in sensors:
            if type(self.d.get(k)) is list:  # Handle list type data.
                if k == 'track':  # Nice display for track sensors.
                    strout = str()
                    #  for tsensor in self.d['track']:
                    #      if   tsensor >180: oc= '|'
                    #      elif tsensor > 80: oc= ';'
                    #      elif tsensor > 60: oc= ','
                    #      elif tsensor > 39: oc= '.'
                    #      #elif tsensor > 13: oc= chr(int(tsensor)+65-13)
                    #      elif tsensor > 13: oc= chr(int(tsensor)+97-13)
                    #      elif tsensor >  3: oc= chr(int(tsensor)+48-3)
                    #      else: oc= '_'
                    #      strout+= oc
                    #  strout= ' -> '+strout[:9] +' ' + strout[9] + ' ' + strout[10:]+' <-'
                    raw_tsens = ['%.1f' % x for x in self.d['track']]
                    strout += ' '.join(raw_tsens[:9]) + '_' + raw_tsens[9] + '_' + ' '.join(raw_tsens[10:])
                elif k == 'opponents':  # Nice display for opponent sensors.
                    strout = str()
                    for osensor in self.d['opponents']:
                        if osensor > 190:
                            oc = '_'
                        elif osensor > 90:
                            oc = '.'
                        elif osensor > 39:
                            oc = chr(int(osensor / 2) + 97 - 19)
                        elif osensor > 13:
                            oc = chr(int(osensor) + 65 - 13)
                        elif osensor > 3:
                            oc = chr(int(osensor) + 48 - 3)
                        else:
                            oc = '?'
                        strout += oc
                    strout = ' -> ' + strout[:18] + ' ' + strout[18:] + ' <-'
                else:
                    strlist = [str(i) for i in self.d[k]]
                    strout = ', '.join(strlist)
            else:  # Not a list type of value.
                if k == 'gear':  # This is redundant now since it's part of RPM.
                    gs = '_._._._._._._._._'
                    p = int(self.d['gear']) * 2 + 2  # Position
                    l = '%d' % self.d['gear']  # Label
                    if l == '-1': l = 'R'
                    if l == '0':  l = 'N'
                    strout = gs[:p] + '(%s)' % l + gs[p + 3:]
                elif k == 'damage':
                    strout = '%6.0f %s' % (self.d[k], bargraph(self.d[k], 0, 10000, 50, '~'))
                elif k == 'fuel':
                    strout = '%6.0f %s' % (self.d[k], bargraph(self.d[k], 0, 100, 50, 'f'))
                elif k == 'speedX':
                    cx = 'X'
                    if self.d[k] < 0: cx = 'R'
                    strout = '%6.1f %s' % (self.d[k], bargraph(self.d[k], -30, 300, 50, cx))
                elif k == 'speedY':  # This gets reversed for display to make sense.
                    strout = '%6.1f %s' % (self.d[k], bargraph(self.d[k] * -1, -25, 25, 50, 'Y'))
                elif k == 'speedZ':
                    strout = '%6.1f %s' % (self.d[k], bargraph(self.d[k], -13, 13, 50, 'Z'))
                elif k == 'z':
                    strout = '%6.3f %s' % (self.d[k], bargraph(self.d[k], .3, .5, 50, 'z'))
                elif k == 'trackPos':  # This gets reversed for display to make sense.
                    cx = '<'
                    if self.d[k] < 0: cx = '>'
                    strout = '%6.3f %s' % (self.d[k], bargraph(self.d[k] * -1, -1, 1, 50, cx))
                elif k == 'stucktimer':
                    if self.d[k]:
                        strout = '%3d %s' % (self.d[k], bargraph(self.d[k], 0, 300, 50, "'"))
                    else:
                        strout = 'Not stuck!'
                elif k == 'rpm':
                    g = self.d['gear']
                    if g < 0:
                        g = 'R'
                    else:
                        g = '%1d' % g
                    strout = bargraph(self.d[k], 0, 10000, 50, g)
                elif k == 'angle':
                    asyms = [
                        "  !  ", ".|'  ", "./'  ", "_.-  ", ".--  ", "..-  ",
                        "---  ", ".__  ", "-._  ", "'-.  ", "'\.  ", "'|.  ",
                        "  |  ", "  .|'", "  ./'", "  .-'", "  _.-", "  __.",
                        "  ---", "  --.", "  -._", "  -..", "  '\.", "  '|."]
                    rad = self.d[k]
                    deg = int(rad * 180 / PI)
                    symno = int(.5 + (rad + PI) / (PI / 12))
                    symno = symno % (len(asyms) - 1)
                    strout = '%5.2f %3d (%s)' % (rad, deg, asyms[symno])
                elif k == 'skid':  # A sensible interpretation of wheel spin.
                    frontwheelradpersec = self.d['wheelSpinVel'][0]
                    skid = 0
                    if frontwheelradpersec:
                        skid = .5555555555 * self.d['speedX'] / frontwheelradpersec - .66124
                    strout = bargraph(skid, -.05, .4, 50, '*')
                elif k == 'slip':  # A sensible interpretation of wheel spin.
                    frontwheelradpersec = self.d['wheelSpinVel'][0]
                    slip = 0
                    if frontwheelradpersec:
                        slip = ((self.d['wheelSpinVel'][2] + self.d['wheelSpinVel'][3]) -
                                (self.d['wheelSpinVel'][0] + self.d['wheelSpinVel'][1]))
                    strout = bargraph(slip, -5, 150, 50, '@')
                else:
                    strout = str(self.d[k])
            out += "%s: %s\n" % (k, strout)
        return out


class DriverAction():
    '''What the driver is intending to do (i.e. send to the server).
    Composes something like this for the server:
    (accel 1)(brake 0)(gear 1)(steer 0)(clutch 0)(focus 0)(meta 0) or
    (accel 1)(brake 0)(gear 1)(steer 0)(clutch 0)(focus -90 -45 0 45 90)(meta 0)'''

    def __init__(self):
        self.actionstr = str()
        # "d" is for data dictionary.
        self.d = {'accel': 0.2,
                  'brake': 0,
                  'clutch': 0,
                  'gear': 1,
                  'steer': 0,
                  'focus': [-90, -45, 0, 45, 90],
                  'meta': 0
                  }

    def clip_to_limits(self):
        """There pretty much is never a reason to send the server
        something like (steer 9483.323). This comes up all the time
        and it's probably just more sensible to always clip it than to
        worry about when to. The "clip" command is still a snakeoil
        utility function, but it should be used only for non standard
        things or non obvious limits (limit the steering to the left,
        for example). For normal limits, simply don't worry about it."""
        self.d['steer'] = clip(self.d['steer'], -1, 1)
        self.d['brake'] = clip(self.d['brake'], 0, 1)
        self.d['accel'] = clip(self.d['accel'], 0, 1)
        self.d['clutch'] = clip(self.d['clutch'], 0, 1)
        if self.d['gear'] not in [-1, 0, 1, 2, 3, 4, 5, 6]:
            self.d['gear'] = 0
        if self.d['meta'] not in [0, 1]:
            self.d['meta'] = 0
        if type(self.d['focus']) is not list or min(self.d['focus']) < -180 or max(self.d['focus']) > 180:
            self.d['focus'] = 0

    def __repr__(self):
        self.clip_to_limits()
        out = str()
        for k in self.d:
            out += '(' + k + ' '
            v = self.d[k]
            if not type(v) is list:
                out += '%.3f' % v
            else:
                out += ' '.join([str(x) for x in v])
            out += ')'
        return out
        return out + '\n'

    def fancyout(self):
        '''Specialty output for useful monitoring of bot's effectors.'''
        out = str()
        od = self.d.copy()
        od.pop('gear', '')  # Not interesting.
        od.pop('meta', '')  # Not interesting.
        od.pop('focus', '')  # Not interesting. Yet.
        for k in sorted(od):
            if k == 'clutch' or k == 'brake' or k == 'accel':
                strout = ''
                strout = '%6.3f %s' % (od[k], bargraph(od[k], 0, 1, 50, k[0].upper()))
            elif k == 'steer':  # Reverse the graph to make sense.
                strout = '%6.3f %s' % (od[k], bargraph(od[k] * -1, -1, 1, 50, 'S'))
            else:
                strout = str(od[k])
            out += "%s: %s\n" % (k, strout)
        return out


