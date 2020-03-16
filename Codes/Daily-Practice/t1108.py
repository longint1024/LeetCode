class Solution:
    def defangIPaddr(self, address: str) -> str:
        ll=len(address)
        s = ""
        for i in range(ll):
            if(address[i]=='.'):
                s=s+"[.]"
            else:
                s=s+address[i]
        return s   