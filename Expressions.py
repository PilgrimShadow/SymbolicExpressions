#AUTH: Jordan Dodson

#TODO: Write _simplified() for the Mult class

class Expression():
  '''The base class for all symbolic expressions'''

  def __init__(self):
    # The set of labels in this expression
    self.labels = set()

  def __add__(self, other):
    z = Add(self, other)
    return z._simplified()

  def __mul__(self, other):
    z = Mult(self, other)
    return z._simplified()

  def deriv(self, wrt=None):
    pass

  def integral(self, wrt=None):
    pass

  def evaluate(self, value_dict):
    pass

  def _simplified(self):
    pass


class Symbol(Expression):
   '''Represents a single symbol'''

   def __init__(self, label):

     self.labels = set([label])

     if isinstance(label, str) and label.isalpha():
       self.label = label
     else:
       raise Exception('Invalid label')

   def __repr__(self):
     return 'Symbol({:s})'.format(self.label)


class Add(Expression):
  '''Represents the addition of two or more sub-expressions'''

  def __init__(self, a, b, *rest):

    self.terms = [a,b] + list(rest)
    self.labels = set()
    for term in self.terms:
      if isinstance(term, Expression):
        self.labels.update(term.labels)

  def _simplified(self):
    to_check = self.terms.copy()
    simplified = []
    counts = {}

    for expr in to_check:
      if isinstance(expr, Symbol):
        counts[expr.label] = 1 + counts.get(expr.label, 0)
      elif isinstance(expr, Add):
        to_check.extend(expr.terms)
      elif isinstance(expr, Mult) and len(expr.terms) == 1 and isinstance(expr.terms[0], Symbol):
        label = list(expr.labels)[0]
        counts[label] = expr.factor + counts.get(label, 0)
      else:
        simplified.append(expr)

    # Group symbols together
    for label, count in counts.items():
      simplified.append(Mult(count, Symbol(label)) if count > 1 else Symbol(label))

    return Add(*simplified) if len(simplified) > 1 else simplified[0]

  def __repr__(self):
    return 'Add({:s})'.format(', '.join(str(term) for term in self.terms))
      

class Mult(Expression):
  '''Represents the product of two or more sub-expressions'''

  def __init__(self, a, b, *rest):
    self.terms = []
    self.factor = 1
    for x in [a,b] + list(rest):
      if isinstance(x, Expression):
        self.terms.append(x)
      elif isinstance(x, float) or isinstance(x, int):
        self.factor *= x
      else:
        raise Exception('Invalid operand')

    self.labels = set()
    for term in self.terms:
      if isinstance(term, Expression):
        self.labels.update(term.labels)


  def __repr__(self):
    return 'Mult({:s})'.format(', '.join(str(term) for term in [self.factor] + self.terms))
